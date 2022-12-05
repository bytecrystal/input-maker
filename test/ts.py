ajew = {}
f = open('ew.txt', encoding = 'utf-8',mode = 'r')
for line in f:
    aj,ew = line.strip('\r\n').split('\t')
    ajew[aj] = float(ew)
f.close()
f = open('../data/new_brief_code.txt', encoding = 'utf-8', mode = 'r')
dz = {}
for line in f:
    z,m = line.strip('\r\n').split('\t')
    if z in dz:
        if len(m) < len(dz[z]):
            dz[z] = m
        else:
            pass
    else:
        dz[z] = m
f.close()
pl1={}
pl2={}
pl3={}
pl4={}
pl5={}
hjzh = ['ah','ai','aj','ak','al','am','an','ao','ap','au','ay','a/','a;','bh','bi','bj','bk','bl','bm','bn','bo','bp','bu','by','b/','b;','ch','ci','cj','ck','cl','cm','cn','co','cp','cu','cy','c/','c;','dh','di','dj','dk','dl','dm','dn','do','dp','du','dy','d/','d;','eh','ei','ej','ek','el','em','en','eo','ep','eu','ey','e/','e;','fh','fi','fj','fk','fl','fm','fn','fo','fp','fu','fy','f/','f;','gh','gi','gj','gk','gl','gm','gn','go','gp','gu','gy','g/','g;','ha','hb','hc','hd','he','hf','hg','hq','hr','hs','ht','hv','hw','hx','hz','ia','ib','ic','id','ie','if','ig','iq','ir','is','it','iv','iw','ix','iz','ja','jb','jc','jd','je','jf','jg','jq','jr','js','jt','jv','jw','jx','jz','ka','kb','kc','kd','ke','kf','kg','kq','kr','ks','kt','kv','kw','kx','kz','la','lb','lc','ld','le','lf','lg','lq','lr','ls','lt','lv','lw','lx','lz','ma','mb','mc','md','me','mf','mg','mq','mr','ms','mt','mv','mw','mx','mz','na','nb','nc','nd','ne','nf','ng','nq','nr','ns','nt','nv','nw','nx','nz','oa','ob','oc','od','oe','of','og','oq','or','os','ot','ov','ow','ox','oz','pa','pb','pc','pd','pe','pf','pg','pq','pr','ps','pt','pv','pw','px','pz','qh','qi','qj','qk','ql','qm','qn','qo','qp','qu','qy','q/','q;','rh','ri','rj','rk','rl','rm','rn','ro','rp','ru','ry','r/','r;','sh','si','sj','sk','sl','sm','sn','so','sp','su','sy','s/','s;','th','ti','tj','tk','tl','tm','tn','to','tp','tu','ty','t/','t;','ua','ub','uc','ud','ue','uf','ug','uq','ur','us','ut','uv','uw','ux','uz','vh','vi','vj','vk','vl','vm','vn','vo','vp','vu','vy','v/','v;','wh','wi','wj','wk','wl','wm','wn','wo','wp','wu','wy','w/','w;','xh','xi','xj','xk','xl','xm','xn','xo','xp','xu','xy','x/','x;','ya','yb','yc','yd','ye','yf','yg','yq','yr','ys','yt','yv','yw','yx','yz','zh','zi','zj','zk','zl','zm','zn','zo','zp','zu','zy','z/','z;',',a',',b',',c',',d',',e',',f',',g',',q',',r',',s',',t',',v',',w',',x',',z','/a','/b','/c','/d','/e','/f','/g','/q','/r','/s','/t','/v','/w','/x','/z',';a',';b',';c',';d',';e',';f',';g',';q',';r',';s',';t',';v',';w',';x',';z']
dkpzh = ['br','bt','ce','ec','mu','my','nu','ny','p/','qz','rb','rv','tb','tv','um','un','vr','vt','wx','xw','ym','yn','zq',',i','/p']
xkpzh = ['qa','za','fb','gb','vb','dc','cd','ed','de','bf','gf','rf','tf','vf','bg','fg','rg','tg','vg','jh','mh','nh','uh','yh','ki','hj','mj','nj','uj','yj','ik','ol','hm','jm','nm','hn','jn','mn','lo',';p','aq','fr','gr','tr','ws','xs','ft','gt','rt','hu','ju','yu','bv','fv','gv','sw','sx','hy','jy','uy','az','k,',';/','p;','/;']
xzgrzh = ['aa','ac','ad','ae','aq','as','aw','ax','az','ca','cq','cz','da','dq','dz','ea','eq','ez','ip','i/','i;','kp','k/','k;','lp','l/','l;','op','o/','o;','pi','pk','pl','po','pp','p;','qa','qc','qd','qe','qq','qs','qw','qx','sa','sq','sz','wa','wq','wz','xa','xq','xz','za','zc','zd','ze','zs','zw','zx','zz',',p',',/',',;','/i','/k','/l','/o','//','/;',';i',';k',';l',';o',';p',';/',';;']
cszh = ['ct',',y','tc','y,','cr',',u','rc','u,','cw',',o','wc','o,','qc',',p','cq','p,','qx','p.','xq','.p','xe','.i','ex','i.','xr','.u','rx','u.','xt','.y','tx','y.']
f = open('zp2.txt', encoding ='utf-8', mode ='r')
for line in f:
    z,p,x = line.strip('\r\n').split('\t')
    x = float(x)
    p = float(p)/1000000000
    if x<=300:
        pl1[z] = p
    elif x<=500:
        pl2[z] = p
    elif x<=1500:
        pl3[z] = p
    elif x<=3000:
        pl4[z] = p
    elif x<=6000:
        pl5[z] = p
f.close()
f = open('jg.txt',encoding = 'utf-8', mode = 'w')
f.write('\t'+'一键'+'\t'+'两键'+'\t'+'三键'+'\t'+'四键'+'\t'+'五键'+'\t'+'选重'+'\t'+'键长'+'\t'+'字均当量'+'\t'+'键均当量'+'\t'+'左右互击'+'\t'+'同指大跨排'+'\t'+'同指小跨排'+'\t'+'小指干扰'+'\t'+'错手'+'\n')
l = [[pl1,'300'],[pl2,'500'],[pl3,'1500'],[pl4,'3000'],[pl5,'6000']]
yl = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0,',':0,'.':0,';':0,'/':0,'\'':0,'_':0,'0':0}
bm = {}
n1a, n2a, n3a, n4a, n5a, xca, jca, zjdla, hja, dkpa, xkpa, xzgra, csa, paa, zjja, p1a, p2a, p3a, p4a, p5a  = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
for i in l:
    n1 = 0
    n2 = 0
    n3 = 0
    n4 = 0
    n5 = 0
    p1=0
    p2=0
    p3=0
    p4=0
    p5=0
    n = [n1,n2,n3,n4,n5]
    hj = 0
    dkp = 0
    xkp = 0
    xzgr = 0
    cs = 0
    xc = 0
    jc = 0
    zjdl = 0
    pa = 0
    zjj=0
    for j in i[0]:
        pa += i[0].get(j,0)
        jc += i[0].get(j,0)*len(dz.get(j,'0000'))
        if dz.get(j,j) not in bm:
            bm[dz.get(j,j)] = 1
        else:
            xc += 1
            if ((int)(i[1]) <= 1500):
                print(dz.get(j,0))
        if len(dz.get(j,'0000')) == 1:
            n1 += 1
            p1+=i[0].get(j,'0000')
        if len(dz.get(j,'0000')) == 2:
            n2 += 1
            p2+=i[0].get(j,'0000')
            if i[1]=='3000' or i[1]=='6000':
                print(j+'\t'+dz[j])
        if len(dz.get(j,'0000')) == 3:
            n3 += 1
            p3+=i[0].get(j,'0000')
        if len(dz.get(j,'0000')) == 4:
            # print(dz.get(j,'0000'))
            n4 += 1
            p4+=i[0].get(j,'0000')
        if len(dz.get(j,'0000')) == 5:
            n5 += 1
            p5+=i[0].get(j,'0000')
        zh = []
        for k in dz.get(j,'0000'):
            yl[k] += i[0].get(j,'0000')
        for k in range(len(dz.get(j,'0000'))-1):
            zh.append(dz.get(j,'0000')[k]+dz.get(j,'0000')[k+1])
        for k in zh:
            zjdl += i[0].get(j,'0000')*ajew[k]
            zjj += i[0].get(j,'0000')
            if k in hjzh or '_' in k:
                hj += i[0].get(j,'0000')
            if k in dkpzh:
                dkp += i[0].get(j,'0000')
            if k in xkpzh:
                xkp += i[0].get(j,'0000')
            if k in xzgrzh:
                xzgr += i[0].get(j,'0000')
            if k in cszh:
                cs += i[0].get(j,'0000')
    jjdl = (zjdl/pa)/((jc/pa)-1)
    print("前" + i[1] + "百选重-----------------------------------------：", xc)
    # print(n4)
    f.write(i[1]+'\t'+str(n1)+'\t'+str(n2)+'\t'+str(n3)+'\t'+str(n4)+'\t'+str(n5)+'\t'+str(xc)+'\t'+str(jc/pa)+'\t'+str(zjdl/pa)+'\t'+str(jjdl)+'\t'+str(hj/zjj)+'\t'+str(dkp/zjj)+'\t'+str(xkp/zjj)+'\t'+str(xzgr/zjj)+'\t'+str(cs/zjj)+'\n')
    n1a += n1
    n2a += n2
    n3a += n3
    n4a += n4
    n5a += n5
    p1a += p1
    p2a += p2
    p3a += p3
    p4a += p4
    p5a += p5
    xca += xc
    jca += jc
    zjdla += zjdl
    hja += hj
    dkpa += dkp
    xkpa += xkp
    xzgra += xzgr
    csa += cs
    paa += pa
    zjja += zjj
jjdla = zjdla/(jca-1)
print('总选重：%d' % xca)
f.write('总计'+'\t'+str(p1a)+'\t'+str(p2a)+'\t'+str(p3a)+'\t'+str(p4a)+'\t'+str(p5a)+'\t'+str(xca)+'\t'+str(jca/paa)+'\t'+str(zjdla/paa)+'\t'+str(jjdla)+'\t'+str(hja/zjja)+'\t'+str(dkpa/zjja)+'\t'+str(xkpa/zjja)+'\t'+str(xzgra/zjja)+'\t'+str(csa/zjja)+'\n')
s = ['q','w','e','r','t','y','u','i','o','p','_']
z = ['a','s','d','f','g','h','j','k','l',';','\'']
x = ['z','x','c','v','b','n','m',',','.','/']
ss=sum(yl.values())
for i in s:
    f.write(i+'\t')
f.write('\n')
for i in s:
    f.write(str(yl[i]/ss)+'\t')
f.write('\n')
for i in z:
    f.write(i+'\t')
f.write('\n')
for i in z:
    f.write(str(yl[i]/ss)+'\t')
f.write('\n')
for i in x:
    f.write(i+'\t')
f.write('\n')
for i in x:
    f.write(str(yl[i]/ss)+'\t')
f.write('\n')
f.close()
