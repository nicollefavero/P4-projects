#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */
const bit<16> TYPE_IPV4 = 0x800;

/* ALTERNATIVE NAME FOR TYPES */
typedef bit<9> egressSpec_t;    // for standard_metadata_t.egress_spec (port) of bmv2 simple switch target
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;


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

header quic_initial_t {
    bit<1> headerForm;
    bit<1> fixedBit;
    bit<2> longPacketType;
    bit<2> reservedBits;
    bit<2> packetNumberLenght;
    bit<32> version;
    bit<8> dstConnIdLength;
    bit<8> srcConnIdLength;
}

// " Destination Connection ID" field (variable-length)
header quic_initial_dstConnId_t {
    varbit<160> dstConnId;
}

// "Source Connection ID" field (variable-length)
header quic_initial_srcConnId_t {
    varbit<160> srcConnId;
}

// "Token Length" and "Token" fields (variable-length and encoded)
header quic_initial_tokenLength_t {
    bit<2> tokenLengthEncoded;
    varbit<62> tokenLength;
}

header quic_initial_token_t {
    varbit<62> token;
}

// "Length" field (variable-length and encoded): "This is the length of the
// remainder of the packet (Packet Number + Payload) in bytes."
header quic_initial_RemainingPacketLength_t {
    bit<2> packetRemainingLengthEncoded;
    varbit<60> payloadLength;
    bit<2> packetNumberLength;  // In bytes (0 - 3). Must add +1 later (1 - 4)
}

// "Packet Number" field (variable-length): "This field is 1 to 4 bytes long.
// The length of the Packet Number field is encoded in the Packet Number length
// bits of byte 0."
header quic_initial_packetNumber_t {
    varbit<32> packetNumber;
}

// "Packet Payload" fields (variable-length)

struct metadata {
    /* empty ??? */
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
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
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            default: accept;
        }
    }
}

/* CHECKSUM VERIFICATION */
control CounterVerifyChecksum(inout headers hdr, inout metadata meta) {
    // TODO: Ver como implementar um checksum para o que eu quero.
    apply { }
}

/* INGRESS PROCESSING */
control CounterIngress(inout headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
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
