CREATE OR REPLACE VIEW tbatting as 
select playerID, sum(G) as bG, sum(AB) as bAB, sum(R) as bR, sum(H) as bH, 
sum(2B) as b2B, sum(3B) as b3B, sum(HR) as bHR, 
sum(RBI) as bRBI, sum(SB) as bSB, sum(CS) as bCS, sum(BB) as bBB, sum(SO) as bSO, sum(IBB) as bIBB, 
sum(HBP) as bHBP, sum(SH) as bSH, sum(SF) as bSF from Batting group by playerID;

CREATE OR REPLACE VIEW tbattingpost as 
select playerID, sum(G) as bpG, sum(AB) as bpAB, sum(R) as bpR, sum(H) as bpH, sum(2B) as bp2B, sum(3B) as bp3B, sum(HR) as bpHR, 
sum(RBI) as bpRBI, sum(SB) as bpSB, sum(CS) as bpCS, sum(BB) as bpBB, sum(SO) as bpSO, sum(IBB) as bpIBB, 
sum(HBP) as bpHBP, sum(SH) as bpSH, sum(SF) as bpSF from BattingPost group by playerID;

CREATE OR REPLACE VIEW tfieldingpost as 
select playerID, sum(POS) as fpPOS, sum(G) as fpG, sum(GS) as fpGS, sum(InnOuts) as fpIO, sum(PO) as fpPO, 
sum(A) as fpA, sum(E) as fpE, sum(DP) as fpDP, sum(TP) as fpTP,
sum(PB) as fpPB, sum(SB) as fpSB, sum(CS) as fpCS
from FieldingPost group by playerID;

CREATE OR REPLACE VIEW tfielding as 
select playerID, sum(POS) as fPOS, sum(G) as fG, sum(GS) as fGS, sum(InnOuts) as fIO, sum(PO) as fPO, 
sum(A) as fA, sum(E) as fE, sum(DP) as fDP, sum(WP) as fWP,
sum(PB) as fPB, sum(SB) as fSB, sum(CS) as fCS, sum(ZR)as fZR
from Fielding group by playerID;

CREATE OR REPLACE VIEW tpitching as 
select playerID, sum(W) as pW, sum(L) as pL, sum(G) as pG, sum(GS) as pGS, sum(CG) as pCG,
sum(SHO) as pSHO, sum(SV) as pSV,
sum(IPouts) as pIP, sum(H) as pH, sum(ER) as pER,
sum(HR) as pHR, sum(BB) as pBB, sum(SO) as pSO, sum(BAOpp)as pBAO,
sum(ERA) as pERA, sum(IBB) as pIBB, sum(WP) as pWP, sum(HBP)as pHBP,
sum(BK) as pBK, sum(BFP) as pBFP, sum(GF) as pGF, sum(R)as pR, sum(SH) as pSH, sum(SF) as pSF
from Pitching group by playerID;

CREATE OR REPLACE VIEW tPitchingPost as 
select playerID, sum(W) as ppW, sum(L) as ppL, sum(G) as ppG, sum(GS) as ppGS, sum(CG) as ppCG, 
sum(SHO) as ppSHO, sum(SV) as ppSV,
sum(IPouts) as ppIP, sum(H) as ppH, sum(ER) as ppER,
sum(HR) as ppHR, sum(BB) as ppBB, sum(SO) as ppSO, sum(BAOpp)as ppBAO,
sum(ERA) as ppERA, sum(IBB) as ppIBB, sum(WP) as ppWP, sum(HBP)as ppHBP,
sum(BK) as ppBK, sum(BFP) as ppBFP, sum(GF) as ppGF, sum(R)as ppR, sum(SH) as ppSH, sum(SF) as ppSF
from PitchingPost group by playerID;

CREATE OR REPLACE VIEW tawards as 
select playerID, sum(awardID) + 1 as award from AwardsPlayers group by playerID;

CREATE OR REPLACE VIEW tNom as 
select playerID, 1 as nom from HallOfFame group by playerID;

CREATE OR REPLACE VIEW tHOF as 
select playerID, 1 as hof from HallOfFame where inducted = 'Y' group by playerID;

CREATE OR REPLACE VIEW tMan as 
select Master.playerID, 1 as tomanager from Master inner join Managers on Master.playerID = Managers.playerID;

CREATE OR REPLACE VIEW player as 
select playerID,nameFirst,nameLast from Master;

CREATE OR REPLACE VIEW treesource as
select player.playerID,bG,bAB,bR,bH,b2B,b3B,bHR,bRBI,bSB,bCS,bBB,bSO,bIBB,bHBP,bSH,bSF,
fPOS,fG,fGS,fIO,fPO,fA,fE,fDP,fWP,fPB,fSB,fCS,fZR,
pW,pL,pG,pGS,pCG,pSHO,pSV,pIP,pH,pER,pHR,pBB,pSO,pBAO,pERA,pIBB,pWP,pHBP,pBK,pBFP,pGF,pR,pSH,pSF,
award,nom,hof,tomanager from player
left outer join tbatting on tbatting.playerID = player.playerID
left outer join tfielding on tfielding.playerID = player.playerID
left outer join tpitching on tpitching.playerID = player.playerID
left outer join tawards on tawards.playerID = player.playerID
left outer join tNom on tNom.playerID = player.playerID
left outer join tHOF on tHOF.playerID = player.playerID
left outer join tMan on tMan.playerID = player.playerID;

CREATE OR REPLACE VIEW battingtree as
select player.playerID,bG,bAB,bR,bH,b2B,b3B,bHR,bRBI,bSB,bCS,bBB,bSO,bIBB,bHBP,bSH,bSF,
award,nom,hof,tomanager from player
left outer join tbatting on tbatting.playerID = player.playerID
left outer join tfielding on tfielding.playerID = player.playerID
left outer join tpitching on tpitching.playerID = player.playerID
left outer join tawards on tawards.playerID = player.playerID
left outer join tNom on tNom.playerID = player.playerID
left outer join tHOF on tHOF.playerID = player.playerID
left outer join tMan on tMan.playerID = player.playerID;

CREATE OR REPLACE VIEW fieldingtree as
select player.playerID,
fPOS,fG,fGS,fIO,fPO,fA,fE,fDP,fWP,fPB,fSB,fCS,fZR,
award,nom,hof,tomanager from player
left outer join tbatting on tbatting.playerID = player.playerID
left outer join tfielding on tfielding.playerID = player.playerID
left outer join tpitching on tpitching.playerID = player.playerID
left outer join tawards on tawards.playerID = player.playerID
left outer join tNom on tNom.playerID = player.playerID
left outer join tHOF on tHOF.playerID = player.playerID
left outer join tMan on tMan.playerID = player.playerID;

CREATE OR REPLACE VIEW pitchingtree as
select player.playerID,
pW,pL,pG,pGS,pCG,pSHO,pSV,pIP,pH,pER,pHR,pBB,pSO,pBAO,pERA,pIBB,pWP,pHBP,pBK,pBFP,pGF,pR,pSH,pSF,
award,nom,hof,tomanager from player
left outer join tbatting on tbatting.playerID = player.playerID
left outer join tfielding on tfielding.playerID = player.playerID
left outer join tpitching on tpitching.playerID = player.playerID
left outer join tawards on tawards.playerID = player.playerID
left outer join tNom on tNom.playerID = player.playerID
left outer join tHOF on tHOF.playerID = player.playerID
left outer join tMan on tMan.playerID = player.playerID;

CREATE OR REPLACE VIEW validtree as
select player.playerID,nameFirst,nameLast,nom,hof,tomanager from player
left outer join tNom on tNom.playerID = player.playerID
left outer join tHOF on tHOF.playerID = player.playerID
left outer join tMan on tMan.playerID = player.playerID;