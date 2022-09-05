$('document').ready(()=>{
    $('#update_fee_btn').click(()=>{
        const checked = $("input[type=checkbox]:checked").length
        if(checked){
            $('#fee_confirmation_modal').modal('show');
        }
        else{
            alert('please select atleast one student to mark as paid')
        }
    })
})