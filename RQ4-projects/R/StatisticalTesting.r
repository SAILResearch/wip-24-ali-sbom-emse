rm(list = ls())

# load packages
library(dplyr)
library(rstatix)

#df1 <- read.csv("E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/CycloneDX_formattedStats.csv")
#df2 <- read.csv("E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/SPDX_formattedStats.csv")


df = read.csv('E:/MITACS/Archive/RQ3/CycloneNSpdxIssueR.csv')
df <- df %>% 
  filter(!is.na(count))

df <- df %>%
  filter(!is.na(format))

df <- df %>%
  filter(!is.na(attribute))

# prepare data for plotting
colnames(df)

df <- df %>% 
  filter(attribute != 'commits')

df <- df %>% 
  filter(attribute != 'packages')

df <- df %>%
  filter(attribute != 'usedBy')

df <- df %>%
  mutate(count = as.numeric(count))

grouped_data <- df %>%
  group_by(format, attribute)

# Perform the Shapiro-Wilk test for normality on each group
shapiro_test_results <- grouped_data %>%
  summarize(shapiro_p_value = shapiro.test(count)$p.value)

shapiro_test_results

df$format <- as.factor(df$format)


df %>% group_by(attribute) %>%
  do(w = wilcox.test(count ~ format, data=., paired=FALSE)) %>% 
  summarise(attribute, Wilcox = p.adjust(w$p.value, method = "bonferroni"))

colnames(df)

#install.packages('coin')
# effect size
df %>% group_by(attribute) %>%
  do(w_ef = wilcox_effsize(data=.,count ~ format, paired = FALSE)) %>%
  summarize(attribute, effect_size = w_ef$effsize)

