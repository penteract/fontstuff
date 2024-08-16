
def isprime(p):
    return p>1 and (p==2 or ( p%2 and all(p%n for n in range(2,int(p**0.5+1))) ))
        
def inbase(n,alph):
    b = len(alph)
    r=[]
    while n>=b:
        r.append(alph[n%b])
        n=n//b
    r.append(alph[n])
    return r
import sys
def makeFactorer(scratch, digs="zero one two three four five six seven eight nine".split()):
    e1,e2 = scratch[-2:] # number ending in e1 mostly means it could be prime
    scratch = scratch[:-2]
    base = len(digs)
    numRems = int(len(scratch)/base)
    res = []
    res.append("@digs"+" = ["+" ".join(digs)+"];")
    def get(dig,rem):
        return scratch[base*rem+dig]
    for (i,d) in enumerate(digs):
        res.append("@Dig"+d+" = ["+ " ".join(scratch[i::base])+"];" ) # get(i,[::])
    for k in range(numRems):
        res.append("@Rem"+str(k)+" = ["+" ".join(scratch[base*k:base*(k+1)])+"];" ) # get([::],k)
    res.append("feature liga {")
    res.append("lookup init{")
    for d in digs:
        res.append(f"sub {d} by {d} {e1} ;")
    res.append("} init;")
    #special case 0 and 1
    res.append("lookup ini2{")
    res.append(f"sub {e1} {digs[0]} {e1}' by {e1} ;")
    res.append(f"sub {e1} {digs[1]} {e1}' by {e1} ;")
    res.append(f"sub {digs[0]} {e1}' by {e2} ;")
    res.append(f"sub {digs[1]} {e1}' by {e2} ;")
    res.append("} ini2;")
    
    res.append("lookup ini3{")
    res.append(f"sub {e1}' @digs by NULL ;")
    res.append("} ini3;")
    for p in range(int(len(scratch)/base)+1):
        if isprime(p):
            # divide
            res.append("lookup d"+str(p)+"{")
            #(rem*base)+dig%p
            for rem in range(p):
                res.append(f"sub @Rem{rem} @digs' by [{' '.join(get(i,(rem*base+i)%p) for i in range(base)) }];")
            #special case dividing p by itself
            inb = inbase(p,digs)
            res.append(f"sub {inb[0]}' {' '.join(inb[1:])} {e1} by {inb[0]} ;")
            res.append(f"sub @digs' by [{' '.join(get(i,i%p) for i in range(base)) }];")
            res.append(f"sub @Rem0 {e1}' by {e2};") 
            res.append("} d"+str(p)+";")
            
            #tidy
            res.append("lookup t"+str(p)+"{")
            for d in digs:
                res.append(f"sub @Dig{d} by {d};")
            res.append("} t"+str(p)+";")
    #TODO: special case 0 and 1
    res.append("} liga;")
    return "\n".join(res)
l = ['uniAB30', 'uniAB31', 'uniAB32', 'uniAB33', 'uniAB34', 'uniAB35', 'uniAB36', 'uniAB37', 'uniAB38', 'uniAB39', 'uniAB3A', 'uniAB3B', 'uniAB3C',
     'uniAB3D', 'uniAB3E', 'uniAB3F', 'uniAB40', 'uniAB41', 'uniAB42', 'uniAB43', 'uniAB44', 'uniAB45', 'uniAB46', 'uniAB47', 'uniAB48', 'uniAB49',
     'uniAB4A', 'uniAB4B', 'uniAB4C', 'uniAB4D', 'uniAB4E', 'uniAB4F', 'uniAB50', 'uniAB51', 'uniAB52', 'uniAB53', 'uniAB54', 'uniAB55', 'uniAB56',
     'uniAB57', 'uniAB58', 'uniAB59', 'uniAB5A', 'uniAB5B', 'uniAB5C', 'uniAB5D', 'uniAB5E', 'uniAB5F', 'uniAB64', 'uniAB65', "question","exclam"]

#import fontTools.feaLib.parser as p
#import fontTools.feaLib.builder as b
if __name__=="__main__":
    #import sys
    import argparse,pathlib
    p = argparse.ArgumentParser()
    #p.add_argument("command",choices=["feature","apply"])
    p.add_argument("--digits",action="store",nargs="+",default="zero one two three four five six seven eight nine".split(),metavar="DIGIT",help="names of digit glyphs")
    p.add_argument("--scratch",action="store",nargs="+",default=l,metavar="GLYPH",help="Specify some glyphs to use as scratch space (will mangle any text using them)")
    p.add_argument("--feature",type=argparse.FileType("w"),metavar="OUTPUT.fea",help="write the feature code to a file")
    p.add_argument("--modify",metavar="FONT.ttf",help="transform an input font")
    p.add_argument("--fontout",type=argparse.FileType("wb"),metavar="FONT.woff2")
    a=p.parse_args()
    #print(a)
    if not (a.feature or a.modify):
        raise Exception("At least one of --feature and --modify must be specified")
    #print(a.scratch)
    f=makeFactorer(a.scratch,a.digits)
    if a.feature:
        a.feature.write(f)
    if(a.modify):
        assert a.fontout
        import fontTools.feaLib.parser
        import fontTools.feaLib.builder 
        import fontTools.ttLib.ttFont
        fnt = fontTools.ttLib.ttFont.TTFont(a.modify)
        from io import StringIO
        fea = fontTools.feaLib.parser.Parser(StringIO(f),fnt.getReverseGlyphMap()).parse()
        fontTools.feaLib.builder.addOpenTypeFeatures(fnt,fea)
        fnt.save(a.fontout)
    #usage="python3"+sys.argv[0]+"""(feature | apply) TODO:  [--font NotoSans-Regular.ttf] [--output out.woff2] [--digits zero one two three four five six seven eight nine] [--scratch uniAB30 ...]"""
    #if len(sys.argv)>1:
    #    if sys.argv[1] == "feature":
    #        pass
        #makeFactorer(l)
        
