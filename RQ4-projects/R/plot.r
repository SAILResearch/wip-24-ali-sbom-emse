#library(ggplot2)
#df <- read.csv("./data_files/CycloneDX_formattedStats.csv")
#print(colnames(df))
#df <- df[!is.na(df$count), ]
#df$count <- as.numeric(df$count)

#plot <- ggplot(df, aes(x=reorder(attribute,-(as.numeric(count))), fill=format)) + 
#  geom_boxplot() +
#  facet_wrap( ~ attribute, scales="free")


#print(plot)
#plot

rm(list = ls())

# load packages
library(dplyr)
library(ggplot2)

df1 <- read.csv("./data_files/CycloneDX_formattedStats.csv")
df2 <- read.csv("./data_files/SPDX_formattedStats.csv")

df <- rbind(df1, df2)

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

data <- 
  df %>%
  group_by(format, attribute) %>%
  summarise(count = sum(count))
colnames(data)

# data$count <- log(data$count)

data <- data %>%
  group_by(attribute) %>%
  mutate(totalCount = sum(count))

plotting_df <-
  data %>% 
  group_by(attribute, format) %>% 
  # a trick! for making a horizontal double sided bar plot
  mutate(count = if_else(format == "SPDX", -count, count))

## find the order
temp_df <-
  plotting_df %>% 
  filter(format == "CycloneDX") %>% 
  arrange(count)

the_order <- temp_df$attribute

plotting_df$hwidth <- ifelse(plotting_df$count > 0, -0, 1)

# plot
p <- 
  plotting_df %>% 
  ggplot(aes(x = attribute, y = count, group = format, fill = format)) +
  geom_bar(stat = "identity", width = 0.6) +
  coord_flip() +
  scale_x_discrete(limits = the_order) + 
  #scale_y_continuous(limits = c(-3.5e06, 3.5e06)) +
  ylim(-2500000, 3100000) + 
  #expand_limits(x = 0, y = -3.5e6) + 
  # 3500000
  geom_text(aes(label =  sprintf("%0.2f%%", abs(count/totalCount)*100)), hjust = plotting_df$hwidth, size = 3) +
  labs(y = "Count") +
  theme(legend.position = "bottom",
        legend.title = element_blank(),
        axis.title.y = element_blank(),
        plot.title = element_text(hjust = 0.5),
        panel.background = element_rect(fill =  "grey90"),
        plot.margin = unit(c(0.1, 0, 0.1, 0), "in")) +
  # reverse the order of items in legend
  # guides(fill = guide_legend(reverse = TRUE)) +
  # change the default colors of bars
  scale_fill_manual(values=c("red", "blue"),
                    name="",
                    breaks=c("SPDX", "CycloneDX"),
                    labels=c("SPDX", "CycloneDX")) 

print(p)
#df(file = "./data_files/tool_metrics.pdf")
dev.off()
p

