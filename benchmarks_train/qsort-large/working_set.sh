#
# Working sets
#
case ${working_set} in
    large)
        local arguments=("input_large.dat")
        local stdouts=("output.out")
        local stderrs=("output.err")
        local outputs=("output.out")
        errno=${global_error_no}
        ;;
    *)
        errno=${global_error_dataset}
        ;;
esac
