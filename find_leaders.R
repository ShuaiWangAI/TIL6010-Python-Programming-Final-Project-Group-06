# Find leaders
library(data.table)
setwd("/Users/shiomiyasuhiro/Library/Mobile Documents/com~apple~CloudDocs/working_files/TUD/ZTD/data_driven_modeling")

# List the file names
files = list.files("data/", pattern = "*_trajectory.csv")

# A function for finding a leader
FindLeader = function(RowDt){
  #browser()
  corrs = which(dt$lane == as.numeric(RowDt[4]) & dt$time == as.numeric(RowDt[13]))
  aheadVehs = which((dt$kp[corrs] - as.numeric(RowDt[7])) < 0)
  if(length(aheadVehs) == 0){
    temp2 = as.data.frame(t(rep(NA, 9)))
    headerNames = paste("leader_",names(dt), sep="")[1:9]
    names(temp2) = headerNames
    return(temp2)
  }else{
    aheadDist = dt$kp[corrs[aheadVehs]] - as.numeric(RowDt[7])
    pointer = aheadVehs[which.max(aheadDist)]
    temp2 = dt[corrs[pointer], 1:9]
    headerNames = paste("leader_",names(dt), sep="")[1:9]
    names(temp2) = headerNames
    return(temp2)
  }
}

# A function for finding a leader
FindLeaderLite = function(RowDt){
  #browser()
  corrs = which(dt$lane == as.numeric(RowDt[4]) & dt$time == as.numeric(RowDt[13]))
  aheadVehs = which((dt$kp[corrs] - as.numeric(RowDt[7])) < 0)
  if(length(aheadVehs) == 0){
    return(NA)
  }else{
    aheadDist = dt$kp[corrs[aheadVehs]] - as.numeric(RowDt[7])
    pointer = aheadVehs[which.max(aheadDist)]
    return(corrs[pointer] + max(0, ii-1-SearchRange))
  }
}

# Parameters
SearchRange = 300

# Loop for files
for(i in 2:length(files)){
  InputFileName = paste("data/", files[i], sep="")
  OutputFileName = paste("data/Paired_", files[i], sep="")
  # Read a data set
  data = fread(InputFileName)
  # Edit headers
  names(data) = c("id", "datetime", "type", "velocity", "lane", "longitude", "latitude", "kp", "length", "error")
  # Edit time format
  data$hh = floor(data$datetime/(10^7))
  data$mm = floor((data$datetime - data$hh*(10^7))/10^5)
  data$ss = (data$datetime - data$hh*10^7 - data$mm*10^5)/10^3
  data$time = data$hh*3600 + data$mm*60 + data$ss
  data$datetime = NULL
  data = subset(data, lane != 3)
  # Sort by time
  data = data[order(data$time),]
  # Temporary data frame for the leaders
  templeaders = NULL
  leaders = NULL
  # Loop for finding leaders
  it = nrow(data)
  for(ii in 1:it){
    if(floor(ii/1000)*1000 == ii) cat("i = ", ii, "\n", sep="")
	if(floor(ii/200000)*200000 == ii){
		cat("Update variables at i = ", ii, "\n", sep="")
		leaders = c(leaders, templeaders)
		templeaders = NULL
	}
    dt = data[max(ii-SearchRange, 1):min(ii+SearchRange, it),]
    if(is.null(templeaders)){
      templeaders = FindLeaderLite(as.matrix(dt[min(SearchRange+1, ii), ]))
    }else{
      templeaders = c(templeaders, FindLeaderLite(as.matrix(dt[min(SearchRange+1, ii), ])))
    }
  }
  leaders = c(leaders, templeaders)
  paired = data[leaders, ]
  names(paired) = paste("leader_",names(data), sep="")
  paired = cbind(data, paired)
  paired = na.omit(paired)
  paired = paired[order(paired$id),]
  write.csv(paired, OutputFileName)
}

# library(parallel)
# max(unlist(mclapply(unique(data$time[4000000:5500000]), function(x){sum(data$time[4000000:5500000] == x)}, mc.cores=4)))
