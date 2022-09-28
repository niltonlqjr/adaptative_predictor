#
# Working sets
#
case ${working_set} in
    small)
        local arguments=("input_small.pgm output_small.smoothing.pgm -c")
        local stdouts=("output.out")
        local stderrs=("output.err")
        local outputs=("output_small.smoothing.pgm")
        errno=${global_error_no}
        ;;
    large)
        local arguments=("input_large.pgm output_large.smoothing.pgm -c")
        local stdouts=("output.out")
        local stderrs=("output.err")
        local outputs=("output_large.smoothing.pgm")
        errno=${global_error_no}
        ;;
    *)
        errno=${global_error_dataset}
        ;;
esac
