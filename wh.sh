TESTS_DIR="./tests/"


function choose_parent_method_window() {
    local METHODS=($(ls -d ${TESTS_DIR}/*/ | xargs -n 1 basename | sed '/^_/d'))
    local whiptail_args=()

    for METHOD in "${METHODS[@]}"; do
        whiptail_args+=("$METHOD" "" "OFF")
    done

    local PARENT_METHOD=$(whiptail --title  "XML-RPC TEST" --radiolist \
        "Choose one- parent method" 0 0 0 \
        "${whiptail_args[@]}" 3>&1 1>&2 2>&3)
        
        if [[ -n "$PARENT_METHOD" ]];  then
            choose_method_window $PARENT_METHOD
        else
            echo "Bye"
        fi
}


function choose_method_window() {
    local PARENT_METHOD="$1"
    local METHODS=($(ls -d ${TESTS_DIR}/$PARENT_METHOD/* | xargs -n 1 basename | sed 's/^test_//; s/.py//; /^_/d'))

    local whiptail_args=()

    for METHOD in "${METHODS[@]}"; do
        whiptail_args+=("$METHOD" "" "OFF")
    done

    local METHOD=$(whiptail --title  "XML-RPC TEST" --radiolist \
        "Choose one.$PARENT_METHOD method" 0 0 0 \
        "${whiptail_args[@]}" 3>&1 1>&2 2>&3)
        
        if [[ -n "$METHOD" ]];  then
            python3 ~/brest/pyone_test/test.py one.$PARENT_METHOD.$METHOD
        else
            choose_parent_method_window
        fi
}



choose_parent_method_window




# grep -Eo '^def test_[a-zA-Z_]+' ./tests/datastore/test_allocate.py | awk '{print $2}' | sed 's/^test_//'




