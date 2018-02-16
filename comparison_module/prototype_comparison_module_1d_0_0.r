#define the filenames - these should be parameterised
in_file_model="C:/Users/User/Dropbox/Work/DIAS/RINGS/BeamModelling/sandbox/test_1d_sin.csv"
in_file_scope="C:/Users/User/Dropbox/Work/DIAS/RINGS/BeamModelling/sandbox/test_1d_sin-rand.csv"

#read the files
df_in_model = read.csv(in_file_model,check.names = FALSE)
df_in_scope = read.csv(in_file_scope,check.names = FALSE)

#merge the dataframes
df_result=merge(df_in_model,df_in_scope,by.x = c("x"),by.y = c("x"), suffixes = c(".model", ".scope"))

#calculate the differences
df_result$differences = df_result$v.model-df_result$v.scope

#plot the two values to the same graph in PNG format
overlaid_out_name=sub(".csv","_overlaid.png",in_file_scope)
png(overlaid_out_name,width = 3,height = 3,res=300,units="in")
plot(df_in_model$x,df_in_model$v,col="red",type = "l",xlab = "Phase (degrees)",ylab = "Value",main="Plot of Model and Telescope data overlaid")
lines(df_in_scope$x,df_in_scope$v,col="blue")
dev.off()

#plot the difference in values to the same graph in PNG format
diffs_out_name=sub(".csv","_diffs.png",in_file_scope)
png(overlaid_out_name,width = 3,height = 3,res=300,units="in")
plot(df_result$x,df_result$differences,xlab = "Phase (degrees)",ylab = "Difference",type="l", main="Plot of difference between Model and Telescope data.")
dev.off()

#calculate and print the RMSE
rmse_out=(mean((df_result$differences^2)))^0.5
print(paste("RMSE = ",rmse_out))

#calculate and print the correlation coefficient
correlation_out = cor(df_result$v.model,df_result$v.scope)
print(paste("Correlation = ",correlation_out))
