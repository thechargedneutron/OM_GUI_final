model Flowsheet
Simulator.Streams.Material_Stream Mat_Stm0(NOC = 0,comp = {});
Simulator.Streams.Material_Stream Mat_Stm1(NOC = 0,comp = {});
Simulator.Streams.Material_Stream Mat_Stm2(NOC = 0,comp = {});
Simulator.Unit_Operations.Flash Flash3(NOC = 0,comp = {} 
equation
Mat_Stm0.compMolFrac[1,:] = {};
Mat_Stm1.compMolFrac[1,:] = {};
Mat_Stm2.compMolFrac[1,:] = {};
end Flowsheet;
