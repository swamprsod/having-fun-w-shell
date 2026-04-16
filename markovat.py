import asyncio as aio, sys, json, random as r, re
from collections import defaultdict as dd
from telethon import TelegramClient as TC, events as ev
from telethon.errors import PeerIdInvalidError as PII
from telethon.tl.types import PeerChannel as PC
from telethon.network import ConnectionTcpMTProxyRandomizedIntermediate as MT

A=2040
H="b18441a1ff607e10a989891a5462e627"
F="markov_model.json"
rapevictims=[-1002036737006,-1002643154443,-1002208940306]
S=7506815256
m=dd(lambda:dd(int))
s=[]
W=2
P=20
R=re.compile(r"ам[её]б[а-я]*|ameb[a-z]*|amoeb[a-z]*", re.IGNORECASE)

def sm():
    dm={}
    for k,v in m.items():
        dm["|".join(k)]=dict(v)
    ds=["|".join(x) for x in s]
    with open(F,"w",encoding="utf-8") as f:
        json.dump({"model":dm,"starts":ds},f,ensure_ascii=False,indent=2)

def lm():
    global m,s
    try:
        with open(F,"r",encoding="utf-8") as f:
            d=json.load(f)
        for ks,tr in d["model"].items():
            k=tuple(ks.split("|"))
            for w,c in tr.items():
                m[k][w]=c
        s=[tuple(x.split("|")) for x in d["starts"]]
        print(f"loadedfrom {F}: {len(m)} states, {len(s)} start")
    except FileNotFoundError:
        print(f"file {F} loadfromblank")

def am(t):
    wds=re.findall(r"\b\w+\b|[^\w\s]", t.lower())
    if len(wds)<W:
        return
    s.append(tuple(wds[:W-1]))
    for i in range(len(wds)-W+1):
        st=tuple(wds[i:i+W-1])
        nx=wds[i+W-1]
        m[st][nx]+=1
    sm()

def gn():
    if not s:
        return None
    st=r.choice(s)
    res=list(st)
    for _ in range(30):
        nx=m.get(st)
        if not nx:
            break
        w=r.choices(list(nx.keys()),weights=list(nx.values()))[0]
        res.append(w)
        st=tuple(res[-W+1:])
    return " ".join(res)

L=aio.new_event_loop()
aio.set_event_loop(L)
ph="95.164.123.219"
pp=8443
ps="3e0e7d5f1011777780b87530e6bcfd29"
cl=TC("markov_psychosis_telethon",A,H,loop=L,connection=MT,proxy=(ph,pp,ps))

async def pc():
    await cl.start()
    for cid in rapevictims:
        try:
            if isinstance(cid,int) and cid<0:
                e=await cl.get_entity(PC(cid))
            else:
                e=await cl.get_entity(cid)
            n=e.title if hasattr(e,'title') else e.first_name
            print(f"loaded: {n} (ID: {cid})")
        except Exception as e:
            print(f"err loading {cid}: {e}")
    await cl.disconnect()

@cl.on(ev.NewMessage(chats=rapevictims))
async def hd(e):
    msg=e.message
    if not msg.text:
        return
    snd=await e.get_sender()
    sid=snd.id if snd else None
    snm=snd.first_name if snd else "???"
    dr="<-" if e.out else "->"
    cn=e.chat.title if hasattr(e.chat,'title') else e.chat.first_name
    print(f"{dr} {snm}: {msg.text}")
    mr=False
    if sid==S:
        mr=True
    else:
        am(msg.text)
        if R.search(msg.text):
            print(f"!!! AMOEBA SYSCALL !!!: {msg.text}")
            mr=True
    if not e.out and (mr or r.random()<(P/100)):
        gen=gn()
        if gen and len(gen.split())>=5:
            print(f"debug: {gen}")
            await msg.reply(gen)

async def mn():
    await cl.start()
    print("listening")
    await cl.run_until_disconnected()

if __name__=="__main__":
    lm()
    L.run_until_complete(pc())
    try:
        L.run_until_complete(mn())
    except KeyboardInterrupt:
        print("\ninterrupt: SIGINT")
    finally:
        L.close()
