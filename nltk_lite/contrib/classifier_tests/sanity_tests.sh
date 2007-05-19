echo 'Zero R test'
python ../classifier/classify.py -f datasets/minigolf/weather
echo 'Zero R verify'
python ../classifier/classify.py -vf datasets/minigolf/weather
echo 'One R test'
python ../classifier/classify.py -a 1R -f datasets/minigolf/weather
echo 'One R verify'
python ../classifier/classify.py -a 1R -vf datasets/minigolf/weather
echo 'Decision Tree test'
python ../classifier/classify.py -a DT -f datasets/test_phones/phoney
echo 'Decision Tree verify'
python ../classifier/classify.py -a DT -vf datasets/minigolf/weather
echo 'Decision Tree with separate training and test'
python ../classifier/classify.py -a DT -t datasets/minigolf/weather -T datasets/minigolf/weather
echo 'Decision Tree with separate training and gold'
python ../classifier/classify.py -a DT -t datasets/minigolf/weather -g datasets/minigolf/weather
echo 'Unsupervised Equal Width'
python ../classifier/discretise.py -a UEW -f datasets/numerical/person -A 1,4,5,6,7 -o 2,3,2,3,4
echo 'Unsupervised Equal Frequency'
python ../classifier/discretise.py -a UEF -t datasets/numerical/person -T datasets/numerical/person -A 1 -o 3
echo 'Naive supervised'
python ../classifier/discretise.py -a NS -t datasets/numerical/weather -T datasets/numerical/weather -g datasets/numerical/weather -A 1
echo 'Naive supervised modified version 1'
python ../classifier/discretise.py -a NS1 -f datasets/numerical/person -A 1,4,5,6,7 -o 2,3,2,3,4
echo 'Naive supervised modified version 2'
python ../classifier/discretise.py -a NS2 -t datasets/numerical/person -T datasets/numerical/person -A 1,4,5,6,7 -o 2,3,2,3,4
echo 'Entropy based supervised'
python ../classifier/discretise.py -a ES -f datasets/numerical/person -A 1,4,5,6,7 -o 2,2,2,2,2
echo 'Rank based feature selection'
python ../classifier/featureselect.py -a RNK -f datasets/minigolf/weather -o IG,2
echo 'Forward Select'
python ../classifier/featureselect.py -a FS -f datasets/minigolf/weather -o DT,3,0
echo 'Backward Select'
python ../classifier/featureselect.py -a BS -f datasets/minigolf/weather -o 1R,4,0.1

