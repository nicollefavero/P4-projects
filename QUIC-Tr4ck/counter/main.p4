#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */
const bit<16> TYPE_IPV4 = 0x800;
const bit<8> PROTOCOL_IPV4_UPD = 8w17;
const bit<2> QUIC_LONG_TYPE_HEADER_INITIAL = 2w0;   // 0x00
const bit<2> QUIC_LONG_TYPE_HEADER_HANDSHAKE = 2w2; // 0x00

#define COUNTER_ENTRIES 8
#define COUNTER_BIT_WIDTH 32
#define THRESHOLD 10

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

struct metadata {
    /* empty ??? */
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    udp_t udp;
    quic_long_t quic_long;
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
            // no default rule: all other packets rejected
        }
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
    bit<32> counter_pos_one; bit<32> counter_pos_two;
    bit<32> counter_val_one; bit<32> counter_val_two;
    bit<1> direction;
    bit<32> aux_min;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action compute_hashes(ip4Addr_t ipAddr1, ip4Addr_t ipAddr2, udpPort_t port1, udpPort_t port2) {
        hash(counter_pos_one,
            HashAlgorithm.crc16,
            (bit<32>) 0,
            {ipAddr1, ipAddr2, port1, port2},
            (bit<32>) COUNTER_ENTRIES
        );

        hash(counter_pos_two,
           HashAlgorithm.crc32,
           (bit<32>) 0,
           {ipAddr1, ipAddr2, port1, port2},
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
            if(hdr.udp.isValid()) {
                direction = 0;
                if(check_ports.apply().hit) {
                    if(direction == 1) {

                        // Computes different hashes for a given client
                        compute_hashes(hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.udp.srcPort, hdr.udp.dstPort);

                        if((hdr.quic_long.headerForm == 1) && (hdr.quic_long.longPacketType == QUIC_LONG_TYPE_HEADER_INITIAL)) {
                            counter_1.read(counter_val_one, counter_pos_one);
                            counter_2.read(counter_val_two, counter_pos_two);

                            if(counter_val_one+1 < counter_val_one+1) {
                                aux_min = counter_val_one+1;
                            } else {
                                aux_min = counter_val_two+1;
                            }

                            // Limits the number of packets coming from the same client
                            if (aux_min > THRESHOLD) {
                                drop();
                            } else {

                                // If the threshold is not passed, forward the packet and increment the sketch
                                counter_1.write(counter_pos_one, counter_val_one+1);
                                counter_2.write(counter_pos_two, counter_val_two+1);
                            }


                        } else if ((hdr.quic_long.headerForm == 1) && (hdr.quic_long.longPacketType == QUIC_LONG_TYPE_HEADER_HANDSHAKE)) {

                            // When a HANDSHAKE packet is received from the client, decrement the sketch
                            counter_1.read(counter_val_one, counter_pos_one);
                            counter_2.read(counter_val_two, counter_pos_two);

                            counter_1.write(counter_pos_one, counter_val_one-1);
                            counter_2.write(counter_pos_two, counter_val_one-1);
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
    apply {}
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
