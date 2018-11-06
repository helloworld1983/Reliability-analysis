#########################################
# Copyright (C) 2016 Project Bonfire    #
#                                       #
# This file is automatically generated! #
#             DO NOT EDIT!              #
#########################################

vlib work

# Include files and compile them

vlog "gate_level_netlist.v"
vlog "/cad/dk/c/v4.11/verilog/c18a6/c18_CORELIB.v"

# vcom "RTL/FIFO_one_hot_CB_comb.vhd"
# vcom "RTL/FIFO_one_hot_CB_Seq.vhd"
# vcom "RTL/FIFO_one_hot_credit_based.vhd"
# vcom "RTL/LBDR.vhd"
# vcom "RTL/arbiter_in.vhd"
# vcom "RTL/arbiter_out.vhd"
# vcom "RTL/allocator.vhd"
# vcom "RTL/xbar.vhd"
# vcom "RTL/Router_32_bit_credit_based_control_part.vhd"
# vcom "RTL/Router_32_bit_credit_based.vhd"

vcom "Packages/TB_Package_Router.vhd"
vcom "Testbench/Router_credit_based_tb.vhd"

# Start the simulation
vsim work.tb_router

# Draw waves
do wave_Router.do
# Run the simulation
run 11000 ns