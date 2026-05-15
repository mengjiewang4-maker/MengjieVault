def export_lsf(positions):

    f=open("structure.lsf","w")

    for x,y in positions:

        f.write(f"""

addcircle;
set("x",{x});
set("y",{y});
set("radius",100e-9);

""")

    f.close()