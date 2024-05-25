# load packages
library(dplyr)
library(ggplot2)

# dataframes
df1 <- read.csv("E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/SPDX_dateCreated.csv")
df2 <- read.csv("E:/MITACS/intern-23-arshdeep/RQ2-Projects/data_files/CycloneDX_dateCreated.csv")

df <- rbind(df1, df2)

# prepare data for plotting
colnames(df)

combined_data <- df %>%
  mutate(Year = as.numeric(format(as.Date(createdDate), "%Y")))

# Group by format and year, then calculate the count of projects in each year
summary_data <- combined_data %>%
  group_by(format, Year) %>%
  summarise(ProjectCount = n()) %>%
  ungroup()

# Print the summary data
print(summary_data, n=29)

summary_data <- summary_data %>%
 filter(Year<=2022)

plot <- ggplot(summary_data, aes(x = Year, y = ProjectCount, color = format, group = format)) +
  geom_line() +
  geom_point() +
  labs(x = "Year",
       y = "Project Count",
       color = "Format") +
  scale_x_continuous(breaks = seq(2008, 2022, by = 1)) +
  theme_minimal()
plot

