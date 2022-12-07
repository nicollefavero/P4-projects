#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */
const bit<16> TYPE_IPV4 = 0x800;
const bit<8> PROTOCOL_IPV4_UPD = 8w17;
const bit<2> QUIC_LONG_TYPE_HEADER_INITIAL = 2w0; // 0x00

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

header quic_t {
    bit<1> headerForm; // indicates if the packet is long (1) or short header (0)
}

header quic_long_t {
    bit<1> fixedBit; // must be set to 1 unless the packet is a VN packet (version negotiation)
    bit<2> longPacketType; // indicates if the packet is VN, Initial, 0-RTT, Handshake or Retry
    bit<2> reservedBits;
    bit<2> packetNumberLength; // In bytes (0 - 3). Must add +1 later (1 - 4)
    bit<32> version;
    bit<8> dstConnIdLength;
}

// " Destination Connection ID" field (variable-length)
header quic_dstConnId_t {
    varbit<160> dstConnId;
}

// "Source Connection ID" field (variable-length)
header quic_srcConnIdLength_t {
    bit<8> srcConnIdLength;
}

header quic_srcConnId_t {
    varbit<160> srcConnId;
    bit<2> tokenLengthEncoded;
}

// "Token Length" and "Token" fields (variable-length and encoded)
header quic_initial_tokenLength_t {
    varbit<62> tokenLength;
}

header quic_initial_token_t {
    varbit<62> token;
}

// "Length" field (variable-length and encoded): "This is the length of the
// remainder of the packet (Packet Number + Payload) in bytes."
// "Packet Number" field (variable-length): "This field is 1 to 4 bytes long.
// The length of the Packet Number field is encoded in the Packet Number length
// bits of byte 0."
header quic_initial_RemainingPacketLength_t {
    bit<2> packetRemainingLengthEncoded;
    varbit<32> packetNumber;  // at least 8 bits (from packetNumberLength)
}

// "Packet Payload" fields (variable-length)
header quic_initial_payload_t {
    varbit<54> payload; // at least 8 bits (from remainingLength - packetNumberLength)
}

struct metadata {
    /* empty ??? */
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    udp_t udp;
    quic_t quic;
    quic_long_t quic_long;
    quic_dstConnId_t quic_dstConnId;
    quic_srcConnIdLength_t quic_srcConnIdLength;
    quic_srcConnId_t quic_srcConnId;
    quic_initial_tokenLength_t quic_initial_tokenLength;
    quic_initial_token_t quic_initial_token;
    quic_initial_RemainingPacketLength_t quic_initial_RemainingPacketLength;
    quic_initial_payload_t quic_initial_payload;
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
        transition parse_quic;
    }

    state parse_quic {
        packet.extract(hdr.quic);
        transition select(hdr.quic.headerForm) {
            // 0: parse_quic_short_h // (if we were parsing short headers too)
            1: parse_quic_long_h;
        }
    }

    state parse_quic_long_h {
        packet.extract(hdr.quic_long);
        if (hdr.quic_long.fixedBit == 1) {
            // parse connection IDs that are variable-length
            packet.extract(hdr.quic_dstConnId, hdr.quic_long.dstConnIdLength);
            packet.extract(hdr.quic_srcConnIdLength);
            packet.extract(hdr.quic_srcConnId, hdr.quic_srcConnIdLength.srcConnIdLength);

            // transition to specific Initial packet parsing
            trasition select(hdr.quic_long.longPacketType) {
                QUIC_LONG_TYPE_HEADER_INITIAL: parse_quic_initial_token;
                // other options: parse 0-RTT (0x01), Handshake (0x02), and Retry (0x03) packets.
            }
        } else {
            transition reject;
            // for when Version Negotiation packets will need to be parsed
            //if (hdr.quic_long.version ==  32w0) {
                //transition parse_quic_vc_packet;
            //}
        }
    }

    state parse_quic_initial_token {
        packet.extract(hdr.quic_initial_tokenLength, hdr.quic_srcConnId.tokenLengthEncoded);

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
