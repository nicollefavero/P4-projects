#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */
const bit<16> TYPE_IPV4 = 0x800;
const bit<8> TYPE_TCP = 6;

/* ALTERNATIVE NAME FOR TYPES */
typedef bit<9> egressSpec_t;    // for standard_metadata_t.egress_spec (port) of bmv2 simple switch target
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;
typedef bit<16> tcpPort_t;


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

header tcp_t {
    tcpPort_t srcPort;
    tcpPort_t dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4> dataOffset;
    bit<4> res;
    bit<1> cwr;
    bit<1> ece;
    bit<1> urg;
    bit<1> ack;
    bit<1> psh;
    bit<1> rst;
    bit<1> syn;
    bit<1> fin;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

struct metadata {
    /* empty ??? */
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    tcp_t tcp;
}

/* PARSER */
parser Parser(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
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
            TYPE_TCP: parse_tcp;
            default: accept;
        }
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }
}

/* CHECKSUM VERIFICATION */
control VerifyChecksum(inout headers hdr, inout metadata meta) {
    // TODO: Ver como implementar um checksum para o que eu quero.
    apply { }
}

/* INGRESS PROCESSING */
control Ingress(inout headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    bit<32> syn_counter = 0;
    bit<32> ack_client_counter = 0;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.pv4.ttl - 1;
    }

    action count_syn_and_ack() {
        if (hdr.tcp.syn == 1) {
            syn_counter = syn_counter + 1;
        }

        if (hdr.tcp.ack == 1 & hdr.ipv4.dstAddr == ???)
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
        // TODO
    }
}
