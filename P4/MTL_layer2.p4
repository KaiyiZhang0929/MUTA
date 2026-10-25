#include <core.p4>
#include <tna.p4>

const bit<16> ETHERTYPE_Planter = 0x1234;
const int<32> one_two_eight = 128;

header ethernet_h {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header Planter_in_h{
    int<32> feature0;
    int<32> feature1;
    int<32> feature2;
    int<32> feature3;
    int<32> feature4;
    int<32> feature5;
    int<32> feature6;
    int<32> feature7;
}


struct header_t {
    ethernet_h   ethernet;
    Planter_in_h    Planter_in;
}

struct metadata_t{
    int<32> tem0_h0;
    int<32> tem0_h1;
    int<32> tem0_h2;
    int<32> tem0_h3;
    int<32> tem0_h4;
    int<32> tem0_h5;
    int<32> tem0_h6;
    int<32> tem0_h7;
    int<32> tem1_h0;
    int<32> tem1_h1;
    int<32> tem1_h2;
    int<32> tem1_h3;
    int<32> tem1_h4;
    int<32> tem1_h5;
    int<32> tem1_h6;
    int<32> tem1_h7;
    int<32> tem2_h0;
    int<32> tem2_h1;
    int<32> tem2_h2;
    int<32> tem2_h3;
    int<32> tem2_h4;
    int<32> tem2_h5;
    int<32> tem2_h6;
    int<32> tem2_h7;
    int<32> tem3_h0;
    int<32> tem3_h1;
    int<32> tem3_h2;
    int<32> tem3_h3;
    int<32> tem3_h4;
    int<32> tem3_h5;
    int<32> tem3_h6;
    int<32> tem3_h7;
}

/*************************************************************************
*********************** Ingress Parser ***********************************
*************************************************************************/

parser SwitchIngressParser(
    packet_in pkt,
    out header_t hdr,
    out metadata_t meta,
    out ingress_intrinsic_metadata_t ig_intr_md) {

    state start {
        pkt.extract(ig_intr_md);
        pkt.advance(PORT_METADATA_SIZE);
        transition parse_ethernet;
    }

    state parse_ethernet {
        pkt.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
        ETHERTYPE_Planter : parse_planter;
        default           : accept;
        }
    }

    state parse_planter {
        pkt.extract(hdr.Planter_in);
        transition accept;
    }
}

/*************************************************************************
*********************** Ingress Deparser *********************************
**************************************************************************/

control SwitchIngressDeparser(
    packet_out pkt,
    inout header_t hdr,
    in metadata_t ig_md,
    in ingress_intrinsic_metadata_for_deparser_t ig_dprsr_md) {
    apply {
        pkt.emit(hdr);
    }
}

/*************************************************************************
*********************** Egress Parser ***********************************
*************************************************************************/

parser SwitchEgressParser(
    packet_in pkt,
    out header_t hdr,
    out metadata_t meta,
    out egress_intrinsic_metadata_t eg_intr_md) {
    state start {
        pkt.extract(eg_intr_md);
        transition accept;
    }
}

/*************************************************************************
*********************** Egress Deparser *********************************
**************************************************************************/

control SwitchEgressDeparser(
    packet_out pkt,
    inout header_t hdr,
    in metadata_t eg_md,
    in egress_intrinsic_metadata_for_deparser_t eg_dprsr_md) {
    apply {
        pkt.emit(hdr);
    }
}

/*************************************************************************
*********************** Ingress Processing********************************
**************************************************************************/

control SwitchIngress(
    inout header_t hdr,
    inout metadata_t meta,
    in ingress_intrinsic_metadata_t ig_intr_md,
    in ingress_intrinsic_metadata_from_parser_t ig_prsr_md,
    inout ingress_intrinsic_metadata_for_deparser_t ig_dprsr_md,
    inout ingress_intrinsic_metadata_for_tm_t ig_tm_md) {

    action drop() {
        ig_dprsr_md.drop_ctl = 0x1;
    }

    action send(PortId_t port) {
        ig_tm_md.ucast_egress_port = port;
    }

    action extract_feature0(int<32> w_0_0, int<32> w_0_1, int<32> w_0_2, int<32> w_0_3, int<32> w_0_4, int<32> w_0_5, int<32> w_0_6, int<32> w_0_7){
        meta.tem0_h0 = meta.tem0_h0 + w_0_0;
        meta.tem0_h1 = meta.tem0_h1 + w_0_1;
        meta.tem0_h2 = meta.tem0_h2 + w_0_2;
        meta.tem0_h3 = meta.tem0_h3 + w_0_3;
        meta.tem0_h4 = meta.tem0_h4 + w_0_4;
        meta.tem0_h5 = meta.tem0_h5 + w_0_5;
        meta.tem0_h6 = meta.tem0_h6 + w_0_6;
        meta.tem0_h7 = meta.tem0_h7 + w_0_7;
    }

    action extract_feature1(int<32> w_1_0, int<32> w_1_1, int<32> w_1_2, int<32> w_1_3, int<32> w_1_4, int<32> w_1_5, int<32> w_1_6, int<32> w_1_7){
        meta.tem0_h0 = meta.tem0_h0 + w_1_0;
        meta.tem0_h1 = meta.tem0_h1 + w_1_1;
        meta.tem0_h2 = meta.tem0_h2 + w_1_2;
        meta.tem0_h3 = meta.tem0_h3 + w_1_3;
        meta.tem0_h4 = meta.tem0_h4 + w_1_4;
        meta.tem0_h5 = meta.tem0_h5 + w_1_5;
        meta.tem0_h6 = meta.tem0_h6 + w_1_6;
        meta.tem0_h7 = meta.tem0_h7 + w_1_7;
    }

    action extract_feature2(int<32> w_2_0, int<32> w_2_1, int<32> w_2_2, int<32> w_2_3, int<32> w_2_4, int<32> w_2_5, int<32> w_2_6, int<32> w_2_7){
        meta.tem1_h0 = meta.tem1_h0 + w_2_0;
        meta.tem1_h1 = meta.tem1_h1 + w_2_1;
        meta.tem1_h2 = meta.tem1_h2 + w_2_2;
        meta.tem1_h3 = meta.tem1_h3 + w_2_3;
        meta.tem1_h4 = meta.tem1_h4 + w_2_4;
        meta.tem1_h5 = meta.tem1_h5 + w_2_5;
        meta.tem1_h6 = meta.tem1_h6 + w_2_6;
        meta.tem1_h7 = meta.tem1_h7 + w_2_7;
    }

    action extract_feature3(int<32> w_3_0, int<32> w_3_1, int<32> w_3_2, int<32> w_3_3, int<32> w_3_4, int<32> w_3_5, int<32> w_3_6, int<32> w_3_7){
        meta.tem1_h0 = meta.tem1_h0 + w_3_0;
        meta.tem1_h1 = meta.tem1_h1 + w_3_1;
        meta.tem1_h2 = meta.tem1_h2 + w_3_2;
        meta.tem1_h3 = meta.tem1_h3 + w_3_3;
        meta.tem1_h4 = meta.tem1_h4 + w_3_4;
        meta.tem1_h5 = meta.tem1_h5 + w_3_5;
        meta.tem1_h6 = meta.tem1_h6 + w_3_6;
        meta.tem1_h7 = meta.tem1_h7 + w_3_7;
    }

    action extract_feature4(int<32> w_4_0, int<32> w_4_1, int<32> w_4_2, int<32> w_4_3, int<32> w_4_4, int<32> w_4_5, int<32> w_4_6, int<32> w_4_7){
        meta.tem2_h0 = meta.tem2_h0 + w_4_0;
        meta.tem2_h1 = meta.tem2_h1 + w_4_1;
        meta.tem2_h2 = meta.tem2_h2 + w_4_2;
        meta.tem2_h3 = meta.tem2_h3 + w_4_3;
        meta.tem2_h4 = meta.tem2_h4 + w_4_4;
        meta.tem2_h5 = meta.tem2_h5 + w_4_5;
        meta.tem2_h6 = meta.tem2_h6 + w_4_6;
        meta.tem2_h7 = meta.tem2_h7 + w_4_7;
    }

    action extract_feature5(int<32> w_5_0, int<32> w_5_1, int<32> w_5_2, int<32> w_5_3, int<32> w_5_4, int<32> w_5_5, int<32> w_5_6, int<32> w_5_7){
        meta.tem2_h0 = meta.tem2_h0 + w_5_0;
        meta.tem2_h1 = meta.tem2_h1 + w_5_1;
        meta.tem2_h2 = meta.tem2_h2 + w_5_2;
        meta.tem2_h3 = meta.tem2_h3 + w_5_3;
        meta.tem2_h4 = meta.tem2_h4 + w_5_4;
        meta.tem2_h5 = meta.tem2_h5 + w_5_5;
        meta.tem2_h6 = meta.tem2_h6 + w_5_6;
        meta.tem2_h7 = meta.tem2_h7 + w_5_7;
    }

    action extract_feature6(int<32> w_6_0, int<32> w_6_1, int<32> w_6_2, int<32> w_6_3, int<32> w_6_4, int<32> w_6_5, int<32> w_6_6, int<32> w_6_7){
        meta.tem3_h0 = meta.tem3_h0 + w_6_0;
        meta.tem3_h1 = meta.tem3_h1 + w_6_1;
        meta.tem3_h2 = meta.tem3_h2 + w_6_2;
        meta.tem3_h3 = meta.tem3_h3 + w_6_3;
        meta.tem3_h4 = meta.tem3_h4 + w_6_4;
        meta.tem3_h5 = meta.tem3_h5 + w_6_5;
        meta.tem3_h6 = meta.tem3_h6 + w_6_6;
        meta.tem3_h7 = meta.tem3_h7 + w_6_7;
    }

    action extract_feature7(int<32> w_7_0, int<32> w_7_1, int<32> w_7_2, int<32> w_7_3, int<32> w_7_4, int<32> w_7_5, int<32> w_7_6, int<32> w_7_7){
        meta.tem3_h0 = meta.tem3_h0 + w_7_0;
        meta.tem3_h1 = meta.tem3_h1 + w_7_1;
        meta.tem3_h2 = meta.tem3_h2 + w_7_2;
        meta.tem3_h3 = meta.tem3_h3 + w_7_3;
        meta.tem3_h4 = meta.tem3_h4 + w_7_4;
        meta.tem3_h5 = meta.tem3_h5 + w_7_5;
        meta.tem3_h6 = meta.tem3_h6 + w_7_6;
        meta.tem3_h7 = meta.tem3_h7 + w_7_7;
    }

    table lookup_feature0 {
        key = { hdr.Planter_in.feature0:exact; }
        actions = {
            extract_feature0();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    table lookup_feature1 {
        key = { hdr.Planter_in.feature1:exact; }
        actions = {
            extract_feature1();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    table lookup_feature2 {
        key = { hdr.Planter_in.feature2:exact; }
        actions = {
            extract_feature2();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    table lookup_feature3 {
        key = { hdr.Planter_in.feature3:exact; }
        actions = {
            extract_feature3();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    table lookup_feature4 {
        key = { hdr.Planter_in.feature4:exact; }
        actions = {
            extract_feature4();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    table lookup_feature5 {
        key = { hdr.Planter_in.feature5:exact; }
        actions = {
            extract_feature5();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    table lookup_feature6 {
        key = { hdr.Planter_in.feature6:exact; }
        actions = {
            extract_feature6();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    table lookup_feature7 {
        key = { hdr.Planter_in.feature7:exact; }
        actions = {
            extract_feature7();
            NoAction;
            }
        size = 256;
        default_action = NoAction;
    }

    apply{
        lookup_feature0.apply();
        lookup_feature1.apply();
        lookup_feature2.apply();
        lookup_feature3.apply();
        lookup_feature4.apply();
        lookup_feature5.apply();
        lookup_feature6.apply();
        lookup_feature7.apply();

        meta.tem0_h0 = meta.tem0_h0 + meta.tem1_h0;
        meta.tem0_h1 = meta.tem0_h1 + meta.tem1_h1;
        meta.tem0_h2 = meta.tem0_h2 + meta.tem1_h2;
        meta.tem0_h3 = meta.tem0_h3 + meta.tem1_h3;
        meta.tem0_h4 = meta.tem0_h4 + meta.tem1_h4;
        meta.tem0_h5 = meta.tem0_h5 + meta.tem1_h5;
        meta.tem0_h6 = meta.tem0_h6 + meta.tem1_h6;
        meta.tem0_h7 = meta.tem0_h7 + meta.tem1_h7;

        meta.tem2_h0 = meta.tem2_h0 + meta.tem3_h0;
        meta.tem2_h1 = meta.tem2_h1 + meta.tem3_h1;
        meta.tem2_h2 = meta.tem2_h2 + meta.tem3_h2;
        meta.tem2_h3 = meta.tem2_h3 + meta.tem3_h3;
        meta.tem2_h4 = meta.tem2_h4 + meta.tem3_h4;
        meta.tem2_h5 = meta.tem2_h5 + meta.tem3_h5;
        meta.tem2_h6 = meta.tem2_h6 + meta.tem3_h6;
        meta.tem2_h7 = meta.tem2_h7 + meta.tem3_h7;

        //add the last two temp value
        meta.tem0_h0 = meta.tem0_h0 + meta.tem2_h0;
        meta.tem0_h1 = meta.tem0_h1 + meta.tem2_h1;
        meta.tem0_h2 = meta.tem0_h2 + meta.tem2_h2;
        meta.tem0_h3 = meta.tem0_h3 + meta.tem2_h3;
        meta.tem0_h4 = meta.tem0_h4 + meta.tem2_h4;
        meta.tem0_h5 = meta.tem0_h5 + meta.tem2_h5;
        meta.tem0_h6 = meta.tem0_h6 + meta.tem2_h6;
        meta.tem0_h7 = meta.tem0_h7 + meta.tem2_h7;

        //clamping function
        if ((meta.tem0_h0 & ~32s0xFFFFFF80) != 0 && meta.tem0_h0[31:31]==1) {meta.tem0_h0 = -128; }
        else if ((meta.tem0_h0 & 32s0xFFFFFF80) != 0 && meta.tem0_h0[31:31]==0) {meta.tem0_h0 = 127; }
        if ((meta.tem0_h1 & ~32s0xFFFFFF80) != 0 && meta.tem0_h1[31:31]==1) {meta.tem0_h1 = -128; }
        else if ((meta.tem0_h1 & 32s0xFFFFFF80) != 0 && meta.tem0_h1[31:31]==0) {meta.tem0_h1 = 127; }
        if ((meta.tem0_h2 & ~32s0xFFFFFF80) != 0 && meta.tem0_h2[31:31]==1) {meta.tem0_h2 = -128; }
        else if ((meta.tem0_h2 & 32s0xFFFFFF80) != 0 && meta.tem0_h2[31:31]==0) {meta.tem0_h2 = 127; }
        if ((meta.tem0_h3 & ~32s0xFFFFFF80) != 0 && meta.tem0_h3[31:31]==1) {meta.tem0_h3 = -128; }
        else if ((meta.tem0_h3 & 32s0xFFFFFF80) != 0 && meta.tem0_h3[31:31]==0) {meta.tem0_h3 = 127; }
        if ((meta.tem0_h4 & ~32s0xFFFFFF80) != 0 && meta.tem0_h4[31:31]==1) {meta.tem0_h4 = -128; }
        else if ((meta.tem0_h4 & 32s0xFFFFFF80) != 0 && meta.tem0_h4[31:31]==0) {meta.tem0_h4 = 127; }
        if ((meta.tem0_h5 & ~32s0xFFFFFF80) != 0 && meta.tem0_h5[31:31]==1) {meta.tem0_h5 = -128; }
        else if ((meta.tem0_h5 & 32s0xFFFFFF80) != 0 && meta.tem0_h5[31:31]==0) {meta.tem0_h5 = 127; }
        if ((meta.tem0_h6 & ~32s0xFFFFFF80) != 0 && meta.tem0_h6[31:31]==1) {meta.tem0_h6 = -128; }
        else if ((meta.tem0_h6 & 32s0xFFFFFF80) != 0 && meta.tem0_h6[31:31]==0) {meta.tem0_h6 = 127; }
        if ((meta.tem0_h7 & ~32s0xFFFFFF80) != 0 && meta.tem0_h7[31:31]==1) {meta.tem0_h7 = -128; }
        else if ((meta.tem0_h7 & 32s0xFFFFFF80) != 0 && meta.tem0_h7[31:31]==0) {meta.tem0_h7 = 127; }

        //give value for the out header
        hdr.Planter_in.feature0 = meta.tem0_h0 + one_two_eight;
        hdr.Planter_in.feature1 = meta.tem0_h1 + one_two_eight;
        hdr.Planter_in.feature2 = meta.tem0_h2 + one_two_eight;
        hdr.Planter_in.feature3 = meta.tem0_h3 + one_two_eight;
        hdr.Planter_in.feature4 = meta.tem0_h4 + one_two_eight;
        hdr.Planter_in.feature5 = meta.tem0_h5 + one_two_eight;
        hdr.Planter_in.feature6 = meta.tem0_h6 + one_two_eight;
        hdr.Planter_in.feature7 = meta.tem0_h7 + one_two_eight;

        send(ig_intr_md.ingress_port);
    }
}
/*************************************************************************
*********************** Egress Processing********************************
**************************************************************************/

control SwitchEgress(inout header_t hdr,
    inout metadata_t meta,
    in egress_intrinsic_metadata_t eg_intr_md,
    in egress_intrinsic_metadata_from_parser_t eg_prsr_md,
    inout egress_intrinsic_metadata_for_deparser_t     eg_dprsr_md,
    inout egress_intrinsic_metadata_for_output_port_t  eg_oport_md) {

    action drop() {
        eg_dprsr_md.drop_ctl = 0x1;
    }

    apply {
    }
}
/*************************************************************************
***********************  S W I T C H  ************************************
*************************************************************************/

Pipeline(SwitchIngressParser(),
    SwitchIngress(),
    SwitchIngressDeparser(),
    SwitchEgressParser(),
    SwitchEgress(),
    SwitchEgressDeparser()) pipe;

Switch(pipe) main;