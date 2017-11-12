########### Compile Master List of Bad Sources with All Info Included ####

# OpenSources$X1 = tolower(OpenSources$X1)
# PolitifactBadSources$`Site name` = tolower(PolitifactBadSources$`Site name`)

install.packages("dplyr")
library("dplyr")



# OpenSources = OpenSources[order(OpenSources$X1), , drop = FALSE]
# PolitifactBadSources = PolitifactBadSources[order(PolitifactBadSources$`Site name`), , drop = FALSE]
# 
# m = matrix(nrow = (833+199), ncol = 9)
# 
# compiledList = as.data.frame(m)

compiledList=compiledList[order(compiledList$site_name),]


compressedList = data.frame(matrix(nrow=(877), ncol = 6))
c = 1
for (row in 1:nrow(compiledList)){
  if(row < nrow(compiledList)){
    if (compiledList[row,1] == compiledList[row+1,1]){
      compressedList[c,] = c(compiledList[row+1,1:4], compiledList[row,5:6])
      c = c + 1
    }
    else if (row > 1){
      if (compiledList[row,1] == compiledList[row - 1,1]){
      }
      else{
        compressedList[c,] = compiledList[row,]
        c = c + 1
      }
    }
    else{
      compressedList[c,] = compiledList[row,]
      c = c + 1
    }
  }
  else{
    if (compiledList[row,1] == compiledList[row - 1,1]){
    }
    else{
      compressedList[c,] = compiledList[row,]
      c = c + 1
    }
  }
}

colnames(compressedList) = colnames(compiledList)

write.csv(x = compressedList, file = "BadSources.csv", row.names = FALSE, quote = FALSE, na = "")

# install.packages("jsonlite")
# library("jsonlite")
# BadSources <- toJSON(compressedList)
# cat(BadSources)
# write_json(BadSources, path = "BadSources.json")
