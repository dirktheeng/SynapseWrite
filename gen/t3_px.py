# XML tags the document scan reacts to, beyond the baseline set
def T3_PX_MORE(e): return [(pat('<wp:exte',e),'T3_EX0',{oi:oi+8}),(pat('<a:blip ',e),'T3_BL0',{oi:oi+8})]
