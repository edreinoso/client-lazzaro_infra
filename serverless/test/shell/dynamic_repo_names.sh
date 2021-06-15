environment="pre"

if [ $environment == "prod" ]; then
    repo='$aws_account_id.dkr.ecr.$aws_default_region.amazonaws.com/lazzaro-front-repo:$ong_name'
else
    repo='$aws_account_id.dkr.ecr.$aws_default_region.amazonaws.com/lazzaro-front-repo-pre:$ong_name'
fi

echo $repo