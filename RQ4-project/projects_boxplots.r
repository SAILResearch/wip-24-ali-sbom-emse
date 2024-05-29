# load packages
library(dplyr)
library(ggplot2)
setwd("/Users/abdulalib/Desktop/Postdoc/Academic/SBOMsWork/DataCollectionNew/arshdeep/RQ4")

df <- read.csv("top200_sample.csv")


gathered_df <- gather(df, attribute, count, -type, -tool_used, -link, -duration, -Commits,  -packages)
gathered_df$link <- NULL
gathered_df$tool_used <- NULL

df <- gathered_df
df <- df %>%
  filter(attribute!="closedIssues") %>%
  filter(attribute!="openIssues") %>%
  filter(attribute!="Commits") 

plot <- ggplot(df, aes(x=reorder(attribute, -(as.numeric(count))), y=log(as.numeric(count)), fill=type)) + 
  geom_boxplot() +
  ylab("Log of Count") + xlab("Github Repository Stats") +
  labs(fill = "Format ") +
  theme(legend.position="top") +
  facet_wrap( ~ attribute, scales="free") +
  theme(
    strip.background = element_blank(),
    strip.text.x = element_blank()
  )

plot

pdf(file = "top200_metrics.pdf",width = 4, height = 3.5)
plot
dev.off()



# WILCOXON STARTS!

df <- gathered_df
names(df)[names(df) == "type"] <- "identifier"

df <- df %>%
  filter(count>=0) 
df <- na.omit(df)

class_spdx <- subset(df, identifier == "SPDX")
class_cdx <- subset(df, identifier == "CycloneDX")
# Perform paired Wilcoxon signed-rank test for each identifier
for (id in unique(df$attribute)) {
  cat("attribute:", id, "\n")
  
  # Subset data for the current identifier
  id_data_A <- as.numeric(subset(class_spdx, attribute == id)$count)
  id_data_B <- as.numeric(subset(class_cdx, attribute == id)$count)
  
  # Perform Wilcoxon signed-rank test
  #print(wilcox.test(id_data_A, id_data_B, paired = FALSE))
  
  mw_test <- wilcox.test(id_data_A, id_data_B, paired = FALSE)
  cat("p-value:", mw_test$p.value, "\n")
  
  # Calculate Cliff's delta
  cliffs_delta <- function(x, y) {
    n1 <- sum(!is.na(x))
    n2 <- sum(!is.na(y))
    sum(ifelse(outer(x, y, "<"), 1, 0)) / (n1 * n2)
  }

  delta <- cliffs_delta(id_data_A, id_data_B)
  cat("cliff's delta:", delta, "\n")
  cat("\n")
}

mean(df$count)
df3 <- df %>%
  group_by(identifier, attribute) %>%
  summarise(mean=mean(as.numeric(count)),
            median = median(as.numeric(count)))


