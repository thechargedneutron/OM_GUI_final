model Flowsheet
Simulator.Streams.Material_Stream Sanidhya(NOC = 0,comp = {});
Simulator.Streams.Material_Stream Beni(NOC = 0,comp = {});
Simulator.Streams.Material_Stream Ashu(NOC = 0,comp = {});
Simulator.Unit_Operations.Flash Flash5(NOC = 0,comp = {} 
equation
Mat_Stm0.compMolFrac[1,:] = {};
Mat_Stm1.compMolFrac[1,:] = {};
Mat_Stm2.compMolFrac[1,:] = {};
connect(Flash5.inlet, Sanidhya.inlet); 
connect(Flash5.outlet, Ashu.outlet); 
connect(Flash5.outlet, Beni.outlet); 
end Flowsheet;
