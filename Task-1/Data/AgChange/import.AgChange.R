
require('rgdal')

polygons = readOGR(dsn='./shapefiles/US_counties_2012_geoid.shp',layer='US_counties_2012_geoid',stringsAsFactors=F,verbose=F)
con = file('./AgCensus_MasterDataFrame.txt','r')
ag1 = readLines(con)
close(con)
ag.data = t(apply(array(ag1),1,function(x){strsplit(x,'\t')[[1]]}))
colnames(ag.data) = ag.data[1,]
ag.data = ag.data[-1,]
counties = polygons
counties@data = data.frame(ag.data[match(polygons@data[,1],ag.data[,grep('FIPS',colnames(ag.data))]),],stringsAsFactors=F)
for (jz in 1:475){
	add.num = as.numeric(counties@data[,jz])
	counties@data[,jz] = add.num
}
print(noquote('Ag Census data successfully imported!'))
print(noquote(paste('Number of counties:',nrow(counties@data),sep=' ')))
print(noquote(paste('Number of variables:',ncol(counties@data),sep=' ')))
