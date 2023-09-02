
#Setup workspace and configure the data table

setwd(#supply your workspace)
data<- read.csv("model_evaluation_all.csv")

head(data)
#one sided t test to see if the distance of sites are significantly smaller than random points 
t.test(data$rdm_distance_mean,mu=na.omit(data$sites_distance_mean),alt="greater",conf=0.95,
       var.eq=F,paired=F)

#one sided t test to see if the flow values of sites are significantly larger than random points 
t.test(data$rdm_flow_mean,mu=na.omit(data$sites_flow_mean),alt="less",conf=0.95,
       var.eq=F,paired=F)


#calculate Z scores
z_score_distance <- (mean(na.omit(data$sites_distance_mean)) - mean(na.omit(data$rdm_distance_mean))) / sd(na.omit(data$rdm_distance_mean))

z_score_distance

z_scores_flow <- (mean(na.omit(data$sites_flow_mean)) - mean(na.omit(data$rdm_flow_mean))) / sd(na.omit(data$rdm_flow_mean))

z_scores_flow


#calculate Z scores with croplands and non croplands
z_score_distance_cropland <- (mean(na.omit(data$cropland_distance_mean)) - mean(na.omit(data$rdm_distance_mean))) / sd(na.omit(data$rdm_distance_mean))

z_score_distance_cropland

z_score_distance_noncropland <- (mean(na.omit(data$non_cropland_distance_mean)) - mean(na.omit(data$rdm_distance_mean))) / sd(na.omit(data$rdm_distance_mean))

z_score_distance_noncropland

z_scores_flow_cropland <- (mean(na.omit(data$cropland_flow_mean)) - mean(na.omit(data$rdm_flow_mean))) / sd(na.omit(data$rdm_flow_mean))

z_scores_flow_cropland

z_scores_flow_noncropland <- (mean(na.omit(data$non_cropland_flow_mean)) - mean(na.omit(data$rdm_flow_mean))) / sd(na.omit(data$rdm_flow_mean))

z_scores_flow_noncropland