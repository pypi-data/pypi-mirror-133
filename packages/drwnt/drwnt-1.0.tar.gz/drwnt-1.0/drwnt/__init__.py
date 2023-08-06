import pygame
def draw_net(win,inps,outs,conns,weights,bias,loc,hid=[]):
    coords={}
    w,h=win.get_size()
    if len(conns)<1:
        raise Exception("Please input at least one connection between nodes")
    if len(inps)==0 or len(outs)==0:
        raise Exception("Please enter lists of outputs or inputs")
    if not loc.lower() in ["rd","ru","ld","lu"]:
        raise Exception("Please enter valid location of the net")
    #outputs
    if loc.lower()=="lu":
        x=105 if len(hid)==0 else 185
        y=25 if max(len(inps),len(outs),len(hid))==len(outs) else (max(len(inps),len(hid))/2*40)-(40*len(outs)/2)+25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[outs[0]]=x-15,y
        for z in range(1,len(outs)):
            y+=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[outs[z]]=x-15,y
    elif loc.lower()=="ld":
        x=105 if len(hid)==0 else 185
        y=h-25 if max(len(inps),len(outs),len(hid))==len(outs) else (h-max(len(inps),len(hid))/2*40)+(40*len(outs)/2)-25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[outs[0]]=x-15,y
        for z in range(1,len(outs)):
            y-=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[outs[z]]=x-15,y
    elif loc.lower()=="ru":
        x=w-25
        y=25 if max(len(inps),len(outs),len(hid))==len(outs) else (max(len(inps),len(hid))/2*40)-(40*len(outs)/2)+25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[outs[0]]=x-15,y
        for z in range(1,len(outs)):
            y+=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[outs[z]]=x-15,y
    elif loc.lower()=="rd":
        x=w-25
        y=h-25 if max(len(inps),len(outs),len(hid))==len(outs) else (h-max(len(inps),len(hid))/2*40)+(40*len(outs)/2)-25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[outs[0]]=x-15,y
        for z in range(1,len(outs)):
            y-=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[outs[z]]=x-15,y
    #inputs
    if loc.lower()=="lu":
        x=25
        y=25 if max(len(inps),len(outs),len(hid))==len(inps) else (max(len(hid),len(outs))/2*40)-(40*len(inps)/2)+25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[inps[0]]=x+15,y
        for z in range(1,len(inps)):
            y+=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[inps[z]]=x+15,y
    elif loc.lower()=="ld":
        x=25
        y=h-25 if max(len(inps),len(outs),len(hid))==len(inps) else (h-max(len(hid),len(outs))/2*40)+(40*len(inps)/2)-25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[inps[0]]=x+15,y
        for z in range(1,len(inps)):
            y-=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[inps[z]]=x+15,y
    elif loc.lower()=="ru":
        x=w-105 if len(hid)==0 else w-185
        y=25 if max(len(inps),len(outs),len(hid))==len(inps) else (max(len(hid),len(outs))/2*40)-(40*len(inps)/2)+25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[inps[0]]=x+15,y
        for z in range(1,len(inps)):
            y+=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[inps[z]]=x+15,y
    elif loc.lower()=="rd":
        x=w-105 if len(hid)==0 else w-185
        y=h-25 if max(len(inps),len(outs),len(hid))==len(inps) else (h-max(len(hid),len(outs))/2*40)+(40*len(inps)/2)-25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords[inps[0]]=x+15,y
        for z in range(1,len(inps)):
            y-=40
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[inps[z]]=x+15,y
    #hidden
    if not len(hid)==0:
        if loc.lower()=="lu":
            x=105
            y=25 if max(len(inps),len(outs),len(hid))==len(hid) else (max(len(inps),len(outs))/2*40)-(40*len(hid)/2)+25
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[hid[0]]=x-15,y
            coords[hid[0]+.1]=x+15,y
            for z in range(1,len(hid)):
                y+=40
                pygame.draw.circle(win,(255,255,255),(x,y),12)
                pygame.draw.circle(win,(0,0,0),(x,y),15,3)
                coords[hid[z]]=x-15,y
                coords[hid[z]+.1]=x+15,y
        elif loc.lower()=="ld":
            x=105
            y=h-25 if max(len(inps),len(outs),len(hid))==len(hid) else (h-max(len(inps),len(outs))/2*40)+(40*len(hid)/2)-25
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[hid[0]]=x-15,y
            coords[hid[0]+.1]=x+15,y
            for z in range(1,len(hid)):
                y-=40
                pygame.draw.circle(win,(255,255,255),(x,y),12)
                pygame.draw.circle(win,(0,0,0),(x,y),15,3)
                coords[hid[z]]=x-15,y
                coords[hid[z]+.1]=x+15,y
        elif loc.lower()=="ru":
            x=w-105
            y=25 if max(len(inps),len(outs),len(hid))==len(hid) else (max(len(inps),len(outs))/2*40)-(40*len(hid)/2)+25
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[hid[0]]=x-15,y
            coords[hid[0]+.1]=x+15,y
            for z in range(1,len(hid)):
                y+=40
                pygame.draw.circle(win,(255,255,255),(x,y),12)
                pygame.draw.circle(win,(0,0,0),(x,y),15,3)
                coords[hid[z]]=x-15,y
                coords[hid[z]+.1]=x+15,y
        elif loc.lower()=="rd":
            x=w-105
            y=h-25 if max(len(inps),len(outs),len(hid))==len(hid) else (h-max(len(inps),len(outs))/2*40)+(40*len(hid)/2)-25
            pygame.draw.circle(win,(255,255,255),(x,y),12)
            pygame.draw.circle(win,(0,0,0),(x,y),15,3)
            coords[hid[0]]=x-15,y
            coords[hid[0]+.1]=x+15,y
            for z in range(1,len(hid)):
                y-=40
                pygame.draw.circle(win,(255,255,255),(x,y),12)
                pygame.draw.circle(win,(0,0,0),(x,y),15,3)
                coords[hid[z]]=x-15,y
                coords[hid[z]+.1]=x+15,y
    #bias node
    if loc.lower()=="lu":
        x=25
        y=25+40*len(inps)+25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords["b"]=x+15,y
    elif loc.lower()=="ld":
        x=25
        y=(h-25)-40*len(inps)-25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords["b"]=x+15,y
    elif loc.lower()=="ru":
        x=w-105 if len(hid)==0 else w-185
        y=25+40*len(inps)+25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords["b"]=x+15,y
    elif loc.lower()=="rd":
        x=w-105 if len(hid)==0 else w-185
        y=(h-25)-40*len(inps)-25
        pygame.draw.circle(win,(255,255,255),(x,y),12)
        pygame.draw.circle(win,(0,0,0),(x,y),15,3)
        coords["b"]=x+15,y
    temp=0
    for x,y in conns:
        if weights[temp]>0:
            color=(255,0,0)
        else:
            color=(0,0,255)
        if not y in outs or len(hid)==0:
            pygame.draw.line(win,color,coords[x],coords[y],4)
        else:
            pygame.draw.line(win,color,coords[x+.1],coords[y],4)
        temp+=1
    for x in bias:
        if x>0:
            color=(255,0,0)
        else:
            color=(0,0,255)
        if bias.index(x)+1>len(outs):
            pygame.draw.line(win,color,coords["b"],coords[hid[bias.index(x)-len(outs)]],4)
        else:
            pygame.draw.line(win,color,coords["b"],coords[outs[bias.index(x)]],4)
    pygame.display.update()