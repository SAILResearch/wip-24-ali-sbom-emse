# Load necessary libraries
library(ggplot2)
library(dplyr)


############################ Code Commit Plot ##################################
# Read the data from a CSV file
data <- read.csv('E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/Top 250 combined Insights/Code commit.csv')

data <- data %>%
  filter(Date >= as.Date("2018-03-26"))

data <- data %>%
  filter(Date <= as.Date("2023-08-01")) %>%
  arrange(Date)
# Convert the 'date' column to a Date format
data$Date <- format(as.Date(data$Date), "%Y-%m")


p <- ggplot(data=data, aes(x = Date, y = Count, group=Format))+
  geom_line(aes(color=Format))+
  geom_point(aes(color=Format)) + 
  theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust = 1, size = 6), 
        axis.text.y = element_text(size = 7),
        axis.title.x = element_text(size = 9), 
        axis.title.y = element_text(size = 9),
        legend.text = element_text(size = 9),
        legend.title = element_text(size = 9)) +
  labs(x = "Year", y = "Code Commits") 

p

############################ Issue Submitted ###################################

spdx_issue <- read.csv('E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/SPDX Top250 Insights/SPDX Submitted Issues.csv')
cdx_issue <- read.csv('E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/CycloneDX Top250 Insights/CycloneDX Submitted Issues.csv')


df <- rbind(spdx_issue, cdx_issue)

new_df <- df %>%
  filter(Date >= as.Date("2018-03-26")) %>%
  arrange(Date)

new_df <- new_df %>%
  filter(Date <= as.Date("2023-08-01")) %>%
  arrange(Date)

new_df$Date <- format(as.Date(new_df$Date), "%Y-%m")

p <- ggplot(data=new_df, aes(x = Date, y = Count, group=Format))+
  geom_line(aes(color=Format))+
  geom_point(aes(color=Format)) + 
  theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust = 1, size = 6), 
        axis.text.y = element_text(size = 7),
        axis.title.x = element_text(size = 9), 
        axis.title.y = element_text(size = 9),
        legend.text = element_text(size = 9),
        legend.title = element_text(size = 9)) +
  labs(x = "Date", y = "Issue Submitted") 
p

############################# PR Submitted #####################################

spdx_pr <- read.csv('E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/SPDX Top250 Insights/SPDX Submitted Patches.csv')
cdx_pr <- read.csv('E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/CycloneDX Top250 Insights/CycloneDX Submitted Patches.csv')


df <- rbind(spdx_pr, cdx_pr)

new_df <- df %>%
  filter(Date >= as.Date("2018-03-26")) %>%
  arrange(Date)

new_df <- new_df %>%
  filter(Date <= as.Date("2023-08-01")) %>%
  arrange(Date)

new_df$Date <- format(as.Date(new_df$Date), "%Y-%m")

p <- ggplot(data=new_df, aes(x = Date, y = Count, group=Format))+
  geom_line(aes(color=Format))+
  geom_point(aes(color=Format)) + 
  theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust = 1, size = 6), 
        axis.text.y = element_text(size = 7),
        axis.title.x = element_text(size = 9), 
        axis.title.y = element_text(size = 9),
        legend.text = element_text(size = 9),
        legend.title = element_text(size = 9)) +
  labs(x = "Date", y = "Pull Requests Submitted") 
p


############################## People Evolution ################################


spdx_people <- read.csv('E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/SPDX Top250 Insights/SPDX People evolution.csv')
cdx_people <- read.csv('E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/CycloneDX Top250 Insights/CycloneDX People evolution.csv')

df <- rbind(spdx_people, cdx_people)

df <- df %>% 
  filter(filters != 'Observers')

new_df <- df %>%
  filter(Date >= as.Date("2018-03-26")) %>%
  arrange(Date)

new_df <- new_df %>%
  filter(Date <= as.Date("2023-08-01")) %>%
  arrange(Date)

new_df$Date <- format(as.Date(new_df$Date), "%Y-%m")

# df_maintainers <- new_df %>% filter(filters == "Maintainers")

# df_users <- new_df %>% filter(filters == "Users")
  
# df_contributors <- new_df %>% filter(filters == "Contributors")

people_plot <- function(data, Y_Label) {
  p <- ggplot(data=data, aes(x = Date, y = Count, group=Format))+
    geom_line(aes(color=Format))+
    geom_point(aes(color=Format)) + 
    theme(legend.position = "bottom",
          axis.text.x = element_text(angle = 45, hjust = 1, size = 6), 
          axis.text.y = element_text(size = 7),
          axis.title.x = element_text(size = 9), 
          axis.title.y = element_text(size = 9),
          legend.text = element_text(size = 9),
          legend.title = element_text(size = 9)) +
    labs(x = "Date", y = Y_Label) 
  p <- p + facet_grid(filters ~ .)
  return(p)
}

# maintainers
# p <- people_plot(df_maintainers, 'Maintainers')
# p

# users
# p <- people_plot(df_users, 'Users')
# p

# Contributors
# p <- people_plot(df_contributors, 'Contributors')
# p

# all
p <- people_plot(new_df, 'People Evolution')
p
