import csv,re,sys
d=sys.argv[1]; out=sys.argv[2]; allout=sys.argv[3] if len(sys.argv)>3 else None
ch={r['id']:r for r in csv.DictReader(open(f'{d}/channels.csv',encoding='utf-8'))}
logo={}
for r in csv.DictReader(open(f'{d}/logos.csv',encoding='utf-8')):
    if not r['feed']: logo.setdefault(r['channel'],r['url'])
for r in csv.DictReader(open(f'{d}/logos.csv',encoding='utf-8')): logo.setdefault(r['channel'],r['url'])
FED={'ChannelOne':'Первый канал','Russia1':'Россия 1','Match':'Матч ТВ','NTV':'НТВ','Channel5':'Пятый канал','RussiaK':'Россия К','Russia24':'Россия 24','Carousel':'Карусель','OTR':'ОТР','TVCentr':'ТВ Центр','RENTV':'РЕН ТВ','Spas':'Спас','STS':'СТС','Domashniy':'Домашний','TV3':'ТВ-3','Pyatnitsa':'Пятница','Zvezda':'Звезда','Mir':'Мир','TNT':'ТНТ','MuzTV':'Муз-ТВ'}
FO=list(FED)
G={'news':'Новости','business':'Новости','weather':'Новости','legislative':'Новости',
 'movies':'Кино и сериалы','series':'Кино и сериалы','classic':'Кино и сериалы',
 'kids':'Детские','animation':'Детские',
 'sports':'Спорт','music':'Музыка',
 'documentary':'Познавательные','education':'Познавательные','science':'Познавательные','travel':'Познавательные','culture':'Познавательные','outdoor':'Познавательные','cooking':'Познавательные','auto':'Познавательные','lifestyle':'Познавательные',
 'entertainment':'Развлекательные','comedy':'Развлекательные','family':'Развлекательные','relax':'Развлекательные','shop':'Развлекательные',
 'religious':'Религиозные','general':'Общие'}
OV={}
def ov(g,names):
    for n in names.split(';'): OV[n.strip()]=g
ov('Познавательные','Discovery Channel;Home 4K;Travel Channel;В мире животных;Живая Планета;Живая природа;Загородная жизнь;Приключения;Неизвестная Россия;Усадьба;Zooпарк;Лапки Live;Big Planet;Просвещение;Большая Азия;Инсайт ТВ;Т24;365 дней ТВ')
ov('Кино и сериалы','.sci-fi;Индия;Кинокомедия;Комедия;Комедийное;НТВ Своя игра;НТВ Следствие вели;Душевное;Про Любовь;Прима;Русь;Время')
ov('Музыка','Fon Music;Zhara;Жара')
ov('Развлекательные','Univer TV;Точка отрыва;Тонус;Сарафан;ТелеДом')
ov('Новости','Царьград ТВ;Соловьёв Live;Красная линия;Svoboda')
ov('Общие','STS International;ТВ Центр International;Первый канал Europa;Мир Kazakhstan;РЖД ТВ;Вместе-РФ;Продвижение;TV PRO;Tochka RF;360°;RTVi;TV BRICS Russian;Конгресс ТВ;ЛДПР ТВ;НТВ Витрина;ОСН;Первый СНГ;Пятый International;РЕН ТВ International;Союзный;Радио 1;Радио России;Закон ТБ;Истоки;8 канал International;Аист ТВ;АИСТ ТВ')
DROP={'RT en Espanol','RT Balkan'}
FIN={'Эфирные':'Федеральные','Общие':'Федеральные','Религиозные':'Федеральные','Международные':'Федеральные',
 'Новости':'Новостные','Фильмы':'Кино и сериалы','Сериалы':'Кино и сериалы','Спорт':'Спортивные',
 'Познавательные':'Познавательные','Природа и путешествия':'Познавательные','Хобби и стиль жизни':'Познавательные',
 'Детские':'Детские','Развлекательные':'Музыкальные / Развлекательные','Музыка':'Музыкальные / Развлекательные','Региональные':'Региональные'}
def final(g,core,base,fed):
    if base in BYTOP: return 'Федеральные'
    if g=='Радио': return 'Новостные' if any(k in core for k in ('Вести','Говорит','России','Радио 1')) else 'Музыкальные / Развлекательные'
    if fed and base=='Carousel': return 'Детские'
    if fed and base=='Russia24': return 'Новостные'
    if fed and base=='MuzTV': return 'Музыкальные / Развлекательные'
    return FIN[g]
FORDER=['Федеральные','Кино и сериалы','Спортивные','Познавательные','Детские','Музыкальные / Развлекательные','Новостные','Ultra HD (4K)','Региональные']
TOP=['Россия 24','РБК-ТВ','РБК','Известия','Кинопремьера','Кинохит','Amedia Hit','viju TV1000 action','Дом кино Премиум','Мосфильм Золотая коллекция','Матч! Премьер','Беларусь 5','KHL Prime','КХЛ','Discovery Channel','Animal Planet','Наука','Моя Планета','viju History','viju Explore','Карусель','Мульт','СТС kids','О!','Мультиландия','Муз-ТВ','РУ.ТВ','Жара HD','Жара','ТНТ Music']
BYTOP=['Belarus1','ONT','STV','Belarus2','Belarus3','Belarus24','STB']
def PRI(c,base,fed,core):
    if c=='by' and base in BYTOP: return BYTOP.index(base)
    if fed and base in FO and 'International' not in core and 'Europa' not in core and 'СНГ' not in core: return 10+FO.index(base)
    if 'International' in core or 'Europa' in core or 'СНГ' in core or 'Kazakhstan' in core: return 300
    if core in TOP: return 50+TOP.index(core)
    return 100
ORDER=['Эфирные','Новости','Фильмы','Сериалы','Детские','Спорт','Познавательные','Природа и путешествия','Развлекательные','Музыка','Хобби и стиль жизни','Общие','Региональные','Международные','Беларусь','Религиозные','Радио']
def refine(g,core,cats,c):
    import re as R
    if g=='Эфирные': return g
    if R.search(r'Радио|Вести FM|Страна FM',core): return 'Радио'
    if core.startswith('Europa Plus'): return 'Музыка'
    if core.startswith('ТНВ'): return 'Региональные'
    if R.search(r'International|Europa|CIS|СНГ|Kazakhstan|Int$|^НТВ Мир',core) and g in ('Общие','Региональные'): return 'Международные'
    if g=='Кино и сериалы':
        return 'Сериалы' if (R.search(r'[Сс]ериал|Serial|Сваты|Скорая|Шеф|Пять минут|Первый отдел|Пёс|Следствие|детектив|роман|бестселлер|Киносерия|Дорама|Остросюжет|ТВ 21|TV 21|Star Family|Fox Life|Своя игра|Душевное|Про Любовь',core) or 'series' in cats and 'movies' not in cats) else 'Фильмы'
    if g in('Познавательные','Развлекательные','Региональные'):
        if R.search(r'охот|[Рр]ыб|Animal|Wild|Дикая|Дикий|Планет|[Пп]рирод|Travel|Туриста|Поехали|стихия|Zoo|Лапки|животн|Приключения|Большая Азия|Живая',core): return 'Природа и путешествия'
        if R.search(r'Кухня|Еда|Вкус|Кулинар|Food|Fashion|Здоров|Доктор|Живи|Авто|Драйв|Телекафе|Home 4K|Ювелир|Shopping|Министерство идей|Усадьба|Загородн|Тонус|ТелеДом|365 дней',core) or set(cats)&{'cooking','auto','lifestyle','shop'}: return 'Хобби и стиль жизни'
    return g
CYR=re.compile('[А-Яа-яЁё]')
import json,os
OVR=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'overrides.json'),encoding='utf-8')) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'overrides.json')) else {'drop':[],'rename':{},'live':[]}
DROPU=set(OVR['drop']);LIVE=set(OVR['live'])
items=[];seen=set()
for c in ['ru','by']:
    L=open(f'{d}/{c}.m3u',encoding='utf-8').read().splitlines();i=0
    while i<len(L):
        if not L[i].startswith('#EXTINF'): i+=1;continue
        inf=L[i];opts=[];i+=1
        while L[i].startswith('#'): opts.append(L[i]);i+=1
        url=L[i].strip();i+=1
        if url in seen or url in DROPU: continue
        seen.add(url)
        m=re.search(r'tvg-id="([^"]*)"',inf);tid=m.group(1) if m else ''
        cid,_,feed=tid.partition('@');name=inf.split(',',1)[1]
        info=ch.get(cid,{})
        if info.get('is_nsfw')=='TRUE': continue
        tags=re.findall(r'\[([^\]]+)\]',name)
        r=re.search(r'\((\d+)[pi]\)',name);res=int(r.group(1)) if r else 0
        core=re.sub(r'\s*\[.*?\]|\s*\(\d+[pi]\)','',name).strip()
        core=re.sub(r' (HD|SD)$','',core)
        base=cid.split('.')[0]
        fed=c=='ru' and base in FED and cid.endswith('.ru')
        alts=[a for a in (info.get('alt_names') or '').split(';') if CYR.search(a)]
        if cid=='STV.by': core='СТВ'
        core={'Belarus-4 Gomel':'Беларусь 4 Гомель','Belarus-4 Vitebsk':'Беларусь 4 Витебск'}.get(core,core)
        if core=='Zhara': core='Жара'
        if fed: core=core.replace(info.get('name','\0'),FED[base]) if info.get('name','\0') in core else FED[base]
        elif alts and core==info.get('name'): core=alts[0]
        cats=[x for x in (info.get('categories') or '').split(';') if x]
        if fed: grp='Эфирные'
        else: grp=next((G[x] for x in cats if x in G),'Региональные')
        if grp=='Общие': grp='Региональные'
        if c=='ru' and core in OV: grp=OV[core]
        if core in DROP: continue
        grp=refine(grp,core,cats,c)
        if c=='by' and grp=='Региональные': grp='Общие'
        grp=final(grp,core,base,fed)
        if c=='by' and re.search(r'^Belarus-4|^Беларусь 4|^Витебск|^Буг-ТВ',core): grp='Региональные'
        if url in OVR['rename']:
            rn,rcid,rg=OVR['rename'][url]; core=rn
            if rcid: cid=rcid; tid=rcid+'@'+(feed or 'SD'); base=rcid.split('.')[0]
            if rg: grp=rg
            fed = grp=='Федеральные' and base in FO
        if grp is None: continue
        key=(c,cid or core.lower(),feed if feed not in('SD','HD','') else '', core.lower())
        score=('cinerama.uz' not in url,url in LIVE,len(tags)==0,res,url.startswith('https'))
        items.append(dict(key=key,score=score,core=core,res=res,tags=tags,grp=grp,tid=tid,cid=cid,opts=opts,url=url,
            sk=(FORDER.index(grp),PRI(c,base,fed,core),core.lower())))
def write(path,its):
    its=sorted(its,key=lambda x:(x['sk'],-x['res'],not x['score'][0],not x['score'][1]))
    cnt={}
    with open(path,'w',encoding='utf-8') as f:
        f.write('#EXTM3U url-tvg="https://iptvx.one/EPG,http://epg.it999.ru/edem.xml.gz" x-tvg-url="https://iptvx.one/EPG,http://epg.it999.ru/edem.xml.gz"\n')
        for x in its:
            n=x['core']+(' HD' if x['res']>=720 else '')
            k=(x['grp'],n);cnt[k]=cnt.get(k,0)+1
            if cnt[k]>1: n+=f' (резерв {cnt[k]-1})'
            f.write(f'#EXTINF:-1 tvg-id="{x["tid"]}" tvg-name="{x["core"]}" tvg-logo="{logo.get(x["cid"],"")}" group-title="{x["grp"]}",{n}\n'+''.join(o+'\n' for o in x['opts'])+f'#EXTGRP:{x["grp"]}\n'+x['url']+'\n')
best={id(x):x for x in items}
fin=list(best.values())
for x in list(fin):
    if False:
        y=dict(x);y['grp']='Ultra HD (4K)';y['sk']=(FORDER.index('Ultra HD (4K)'),0,x['core'].lower());fin.append(y)
write(out,fin)
if allout: write(allout,items)
print(len(best),len(items))
from collections import Counter;print(Counter(x['grp'] for x in best.values()))
