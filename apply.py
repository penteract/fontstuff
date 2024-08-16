if __name__=="__main__":
    import argparse,pathlib
    p = argparse.ArgumentParser()
    #p.add_argument("command",choices=["feature","apply"])
    p.add_argument("feature",type=open,metavar="FEATURE.fea",help="input feature")
    p.add_argument("font",metavar="FONT.ttf",help="transform an input font")
    p.add_argument("out",type=argparse.FileType("wb"),metavar="FONT.woff2")
    a=p.parse_args()
    #print(a)
    import fontTools.feaLib.parser
    import fontTools.feaLib.builder 
    import fontTools.ttLib.ttFont
    fnt = fontTools.ttLib.ttFont.TTFont(a.font)
    fea = fontTools.feaLib.parser.Parser(a.feature,fnt.getReverseGlyphMap()).parse()
    fontTools.feaLib.builder.addOpenTypeFeatures(fnt,fea)
    fnt.save(a.out)
        
