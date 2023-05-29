#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */
const bit<16> TYPE_IPV4 = 0x800;
const bit<8> PROTOCOL_IPV4_UPD = 8w17;
const bit<8> PROTOCOL_IPV4_TEL = 8w18; //definition for telemetry
const bit<2> QUIC_LONG_TYPE_HEADER_INITIAL = 2w0;   // 0x00
const bit<2> QUIC_LONG_TYPE_HEADER_HANDSHAKE = 2w2; // 0x00

#define COUNTER_ENTRIES 8
#define COUNTER_BIT_WIDTH 32
#define THRESHOLD 10
#define THRESHOLD_2 5
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1

const bit<32> TYPE_READ = 0x0606;
const bit<32> TYPE_SNAPSHOT = 0x0607;
const bit<32> TYPE_UPDATE = 0x0608;
const bit<32> TYPE_EXPORT = 0x0609;

/* ALTERNATIVE NAME FOR TYPES */
typedef bit<9> egressSpec_t;    // for standard_metadata_t.egress_spec (port) of bmv2 simple switch target
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;
typedef bit<16> udpPort_t;


/* HEADERS */
header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4> version;
    bit<4> ihl;
    bit<8> diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3> flags;
    bit<13> fragOffset;
    bit<8> ttl;
    bit<8> protocol;
    bit<16> hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header udp_t {
    udpPort_t srcPort;
    udpPort_t dstPort;
    bit<16> packetLength;
    bit<16> checksum;
}

header quic_long_t {
    bit<1> headerForm;
    bit<1> fixedBit;
    bit<2> longPacketType;
    bit<2> reservedBits;
    bit<2> packetNumberLength;
}

header telemetry_t{
    bit<32> type;
    bit<32> sw;
    bit<32> flowid_1;
    bit<32> flowid_2;
    bit<32> field;
}

struct metadata {
    bit<32> connection_state;
    bit<32> table_input;
    bit<32> counter_pos_one_f; bit<32> counter_pos_two_f;
    bit<32> counter_val_one; bit<32> counter_val_two;
    bit<32> counter_pos_one_b; bit<32> counter_pos_two_b;
    bit<32> direction;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    udp_t udp;
    quic_long_t quic_long;
    telemetry_t telemetry;
}

/* PARSER */
parser CounterParser(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            // no default rule: all other packets rejected
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            PROTOCOL_IPV4_UPD: parse_udp;
            PROTOCOL_IPV4_TEL: parse_telemetry;
            // no default rule: all other packets rejected
        }
    }

    state parse_telemetry {
        packet.extract(hdr.telemetry);
        transition accept;
    }

    state parse_udp {
        packet.extract(hdr.udp);
        transition parse_quic_long;
    }


    state parse_quic_long {
        packet.extract(hdr.quic_long);
        transition accept;
    }
}

/* CHECKSUM VERIFICATION */
control CounterVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

/* INGRESS PROCESSING */
control CounterIngress(inout headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    register<bit<COUNTER_BIT_WIDTH>>(COUNTER_ENTRIES) counter_1;
    register<bit<COUNTER_BIT_WIDTH>>(COUNTER_ENTRIES) counter_2;

    bit<32> aux_min;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action clone_packet() {
      const bit<32> REPORT_MIRROR_SESSION_ID = 500;
      clone(CloneType.I2E, REPORT_MIRROR_SESSION_ID);
    }

    action compute_hashes_forward(ip4Addr_t ipAddr1, ip4Addr_t ipAddr2) {
        hash(meta.counter_pos_one_f,
            HashAlgorithm.crc16,
            (bit<32>) 0,
            {ipAddr1, ipAddr2},
            (bit<32>) COUNTER_ENTRIES
        );

        hash(meta.counter_pos_two_f,
           HashAlgorithm.crc32,
           (bit<32>) 0,
           {ipAddr2, ipAddr1},
           (bit<32>) COUNTER_ENTRIES
        );
    }

    action compute_hashes_backward(ip4Addr_t ipAddr1, ip4Addr_t ipAddr2) {
        hash(meta.counter_pos_one_b,
            HashAlgorithm.crc16,
            (bit<32>) 0,
            {ipAddr2, ipAddr1},
            (bit<32>) COUNTER_ENTRIES
        );

        hash(meta.counter_pos_two_b,
           HashAlgorithm.crc32,
           (bit<32>) 0,
           {ipAddr1, ipAddr2},
           (bit<32>) COUNTER_ENTRIES
        );
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    action set_direction(bit<1> dir) {
        direction = dir;
    }

    table check_ports {
        key = {
            standard_metadata.ingress_port: exact;
            standard_metadata.egress_spec: exact;
        }
        actions = {
            set_direction;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }

        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }

        size = 1024;
        default_action = drop();
    }

    apply {
        if(hdr.ipv4.isValid()) {
            ipv4_lpm.apply();
            if(hdr.telemetry.isValid()) {
                 if(hdr.telemetry.type == TYPE_READ){
                     compute_hashes_backward(hdr.telemetry.flowid_1, hdr.telemetry.flowid_2);
                     counter_2.read(hdr.telemetry.field, meta.counter_pos_one_b);
                     hdr.telemetry.type = TYPE_EXPORT;
                 }
                 if(hdr.telemetry.type == TYPE_UPDATE){
                     counter_1.write(hdr.telemetry.flowid_1, hdr.telemetry.field);
                 }
            }
            else if(hdr.udp.isValid()) {
                meta.direction = 0;
                if(check_ports.apply().hit) {
                    if(meta.direction == 1) {
                        // Computes different hashes for a given client
                        compute_hashes_forward(hdr.ipv4.srcAddr, hdr.ipv4.dstAddr);
                        counter_1.read(meta.counter_val_one, meta.counter_pos_one_f);
                        counter_2.read(meta.counter_val_two, meta.counter_pos_two_b);
                        if((hdr.quic_long.headerForm == 1) && (hdr.quic_long.longPacketType == QUIC_LONG_TYPE_HEADER_INITIAL)) {

                            /*
                            if(counter_val_one+1 < counter_val_one+1) {
                                aux_min = counter_val_one+1;
                            } else {
                                aux_min = counter_val_two+1;
                            }*/

                            meta.connection_state = meta.counter_val_one - 2*meta.counter_val_two;
                            // Limits the number of packets coming from the same client
                            if (meta.connection_state > THRESHOLD) {
                                drop();
                            } else {
                                if (meta.connection_state > THRESHOLD_2){
                                     clone_packet();
                                }
                                // If the threshold is not passed, forward the packet and increment the sketch
                                counter_1.write(meta.counter_pos_one_f, meta.counter_val_one+1);
                                //counter_2.write(counter_pos_two, counter_val_two+1);
                            }
                        }
                    }

                    // Drop packets from server
                    if(meta.direction == 0) {
                        compute_hashes_backward(hdr.ipv4.srcAddr, hdr.ipv4.dstAddr);

                        counter_1.read(meta.counter_val_one, meta.counter_pos_one_b);
                        counter_2.read(meta.counter_val_two, meta.counter_pos_two_b);
                       if ((hdr.quic_long.headerForm == 1) && (hdr.quic_long.longPacketType == QUIC_LONG_TYPE_HEADER_HANDSHAKE)) {
                            // When a HANDSHAKE packet is received from the client, decrement the sketch
                            //counter_1.write(counter_pos_one, counter_val_one-1);
                            counter_2.write(meta.counter_pos_two_b, meta.counter_val_two+1);
                        }
                    }
                }
            }
        }
    }
}

/* EGRESS PROCESSING */
control CounterEgress(inout headers hdr,
               inout metadata meta,
               inout standard_metadata_t standard_metadata) {

    bit<32> this_switch_id;

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    action switch_id(bit<32> id){
        this_switch_id = id;
    }


    table id_exact {
        key = {
            meta.table_input : exact;
        }

        actions = {
            ipv4_forward;
            switch_id;
        }
        size = 1024;
    }

    apply {
        // In case the "instance type" is a cloned packet, send to the controller
        if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_CLONE) {
             hdr.telemetry.setValid();
             meta.table_input = 100;
             id_exact.apply();
             hdr.telemetry.type = TYPE_SNAPSHOT;
             hdr.telemetry.field = meta.connection_state;
             hdr.telemetry.sw = this_switch_id;
             hdr.telemetry.flowid_1 = hdr.ipv4.srcAddr;
             hdr.telemetry.flowid_2 = hdr.ipv4.dstAddr;
             hdr.ipv4.protocol = 18;
        }
    }
}

/* CHECKSUM COMPUTATION */
control CounterComputeChecksum(inout headers hdr,
                        inout metadata meta) {
    apply {
        update_checksum(
            hdr.ipv4.isValid(),
            {
                hdr.ipv4.version,
                hdr.ipv4.ihl,
                hdr.ipv4.diffserv,
                hdr.ipv4.totalLen,
                hdr.ipv4.identification,
                hdr.ipv4.flags,
                hdr.ipv4.fragOffset,
                hdr.ipv4.ttl,
                hdr.ipv4.protocol,
                hdr.ipv4.srcAddr,
                hdr.ipv4.dstAddr
            },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16
        );
    }
}

/* DEPARER */
control CounterDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.telemetry);
        packet.emit(hdr.udp);
        packet.emit(hdr.quic_long);
    }
}

/* SWITCH */
V1Switch(
    CounterParser(),
    CounterVerifyChecksum(),
    CounterIngress(),
    CounterEgress(),
    CounterComputeChecksum(),
    CounterDeparser()
) main;
