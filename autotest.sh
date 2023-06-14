if [ ! -d "../reports" ]; then
    mkdir -p "../reports"
fi

pytest --html=../reports/report.html