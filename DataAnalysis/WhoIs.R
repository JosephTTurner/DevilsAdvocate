######## Frequency Plot of Locations in Politifact data ############

par(mar=c(11,2,1,0), mgp=c(-1,0,-1))
barplot(table(PolitiFact$pf_registration), las = 2, cex.names = 1)
