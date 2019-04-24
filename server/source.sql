CREATE VIEW tbatting as 
select playerID, sum(G) as bG, sum(AB) as bAB, sum(R) as bR, sum(H) as bH, 
sum(2B) as b2B, sum(3B) as b3B, sum(HR) as bHR, 
sum(RBI) as bRBI, sum(SB) as bSB, sum(CS) as bCS, sum(BB) as bBB, sum(SO) as bSO, sum(IBB) as bIBB, 
sum(HBP) as bHBP, sum(SH) as bSH, sum(SF) as bSF from batting group by playerID;

CREATE VIEW tbattingpost as 
select playerID, sum(G) as bpG, sum(AB) as bpAB, sum(R) as bpR, sum(H) as bpH, sum(2B) as bp2B, sum(3B) as bp3B, sum(HR) as bpHR, 
sum(RBI) as bpRBI, sum(SB) as bpSB, sum(CS) as bpCS, sum(BB) as bpBB, sum(SO) as bpSO, sum(IBB) as bpIBB, 
sum(HBP) as bpHBP, sum(SH) as bpSH, sum(SF) as bpSF from battingpost group by playerID;

CREATE VIEW tfieldingpost as 
select playerID, sum(POS) as fpPOS, sum(G) as fpG, sum(GS) as fpGS, sum(InnOuts) as fpIO, sum(PO) as fpPO, 
sum(A) as fpA, sum(E) as fpE, sum(DP) as fpDP, sum(TP) as fpTP,
sum(PB) as fpPB, sum(SB) as fpSB, sum(CS) as fpCS
from fieldingpost group by playerID;

CREATE VIEW tfielding as 
select playerID, sum(POS) as fPOS, sum(G) as fG, sum(GS) as fGS, sum(InnOuts) as fIO, sum(PO) as fPO, 
sum(A) as fA, sum(E) as fE, sum(DP) as fDP, sum(WP) as fWP,
sum(PB) as fPB, sum(SB) as fSB, sum(CS) as fCS, sum(ZR)as fZR
from fielding group by playerID;

CREATE VIEW tpitching as 
select playerID, sum(W) as pW, sum(L) as pL, sum(G) as pG, sum(GS) as pGS, sum(CG) as pCG,
sum(SHO) as pSHO, sum(SV) as pSV,
sum(IPouts) as pIP, sum(H) as pH, sum(ER) as pER,
sum(HR) as pHR, sum(BB) as pBB, sum(SO) as pSO, sum(BAOpp)as pBAO,
sum(ERA) as pERA, sum(IBB) as pIBB, sum(WP) as pWP, sum(HBP)as pHBP,
sum(BK) as pBK, sum(BFP) as pBFP, sum(GF) as pGF, sum(R)as pR, sum(SH) as pSH, sum(SF) as pSF
from Pitching group by playerID;

CREATE VIEW tPitchingPost as 
select playerID, sum(W) as ppW, sum(L) as ppL, sum(G) as ppG, sum(GS) as ppGS, sum(CG) as ppCG, 
sum(SHO) as ppSHO, sum(SV) as ppSV,
sum(IPouts) as ppIP, sum(H) as ppH, sum(ER) as ppER,
sum(HR) as ppHR, sum(BB) as ppBB, sum(SO) as ppSO, sum(BAOpp)as ppBAO,
sum(ERA) as ppERA, sum(IBB) as ppIBB, sum(WP) as ppWP, sum(HBP)as ppHBP,
sum(BK) as ppBK, sum(BFP) as ppBFP, sum(GF) as ppGF, sum(R)as ppR, sum(SH) as ppSH, sum(SF) as ppSF
from PitchingPost group by playerID;

CREATE VIEW tawards as 
select playerID, sum(awardID) + 1 as award from AwardsPlayers group by playerID;

CREATE VIEW tNom as 
select playerID, 1 as nom from HallOfFame group by playerID;

CREATE VIEW tHOF as 
select playerID, 1 as hof from HallOfFame where inducted = 'Y' group by playerID;

CREATE VIEW tMan as 
select master.playerID, 1 as tomanager from master inner join Managers on master.playerID = Managers.playerID;

CREATE VIEW player as 
select playerID from master;

Create VIEW treesource as
select player.playerID,bG,bAB,bR,bH,b2B,b3B,bHR,bRBI,bSB,bCS,bBB,bSO,bIBB,bHBP,bSH,bSF,
bpG,bpAB,bpR,bpH,bp2B,bp3B,bpHR,bpRBI,bpSB,bpCS,bpBB,bpSO,bpIBB,bpHBP,bpSH,bpSF,
fPOS,fG,fGS,fIO,fPO,fA,fE,fDP,fWP,fPB,fSB,fCS,fZR,
fpPOS,fpG,fpGS,fpIO,fpPO,fpA,fpE,fpDP,fpTP,fpPB,fpSB,fpCS,
pW,pL,pG,pGS,pCG,pSHO,pSV,pIP,pH,pER,pHR,pBB,pSO,pBAO,pERA,pIBB,pWP,pHBP,pBK,pBFP,pGF,pR,pSH,pSF,
ppW,ppL,ppG,ppGS,ppCG,ppSHO,ppSV,ppIP,ppH,ppER,ppHR,ppBB,ppSO,ppBAO,ppERA,ppIBB,ppWP,ppHBP,
ppBK,ppBFP,ppGF,ppR,ppSH,ppSF,award,nom,hof,tomanager from player
left outer join tbatting on tbatting.playerID = player.playerID
left outer join tbattingpost on tbattingpost.playerID = player.playerID
left outer join tfielding on tfielding.playerID = player.playerID
left outer join tfieldingpost on tfieldingpost.playerID = player.playerID
left outer join tpitching on tpitching.playerID = player.playerID
left outer join tPitchingPost on tPitchingPost.playerID = player.playerID
left outer join tawards on tawards.playerID = player.playerID
left outer join tNom on tNom.playerID = player.playerID
left outer join tHOF on tHOF.playerID = player.playerID
left outer join tMan on tMan.playerID = player.playerID;


Create VIEW treesource2 as
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