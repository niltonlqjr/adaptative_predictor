#
# Working sets
#
case ${working_set} in
    small)
        local arguments=("75000")
        local stdouts=("output.out")
        local stderrs=("output.err")
        local outputs=("output.out")
        errno=${global_error_no}
        ;;
    *)
        errno=${global_error_dataset}
        ;;
esac
