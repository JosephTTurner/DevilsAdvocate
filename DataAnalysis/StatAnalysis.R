setwd("C:/workspace/DevilsAdvocate/DataAnalysis")
workingDir = getwd()

####### Parallels methods demonstrated in 
####### "The Language that Gets People to Give:
####### Phrases that Predict Success on Kickstarter"


## Penalized Logistic Regression ##
# "Penalized logistic regression ... guards against collinearity
# and sparsity..."
# "The regression technique handles this by moving the coefficient's 
# weight to the most predictive feature."
# "Thus we use an R implementation of penalized logistic regression
# with ten fold cross-validation, cv.glmnet to handle
# phrase collinearity and guard against overfitting."
# https://cran.r-project.org/web/packages/glmnet/

install.packages("glmnet")
library("glmnet")

# Input is assumed to be an article that has been 
# parsed to fit a bag of words model 
# with tags for phrases (already determined)
# and dependent binary variables "bias" and "fake" (to be assigned)

# The model will be derived from a large collection of
# phrases that have arleady been tagged. 

modelData = data.frame(SmallTestData)

attach(modelData)

lmModel = lm(data=modelData, fake~.)
plot(fake~p2, col = "green")
abline(lm(fake ~ p2), col = "red")
points(fake~bias, col="blue")

summary(lmModel)

plot(lmModel)

model = glmnet(x=modelData, y=fake, family="binomial")



