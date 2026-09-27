for program in ./programs/*; do
    p=$(basename $program .s)
    for config in ./configurations/*; do
        c=$(basename $config .txt)
        python main.py -p $program -c $config > ./outputs/p${p}_c${c}.txt
    done
done
