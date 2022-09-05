
function reveal(id,id1){
    id.classList.toggle('fa-eye-slash')
    const input = document.getElementById(id1)

    if(input.type=="text"){
        input.type="password"
    }
    else{
        input.type="text"
    }
}



const main = () =>{
    $('#userid').on('focusout',()=>{
        const username = $('#userid').val()
        $('#userid + i').addClass('fa-spinner')
        $('#userid + i').removeClass('fa-times-circle')
        $('#userid + i').removeClass('fa-check-circle')
        $('#userid + i').css('transform','scale(1)')
        const icon = document.getElementById('icon')
        icon.style.animation = "spin 1s infinite ease-in-out"
        $.ajax({
            type:'get',
            url:'/accounts/login/checkloginusername/',
            data:{
                username:username
            },
            success:function(response){
                if(response['error']){
                    $('#userid + i').removeClass('fa-spinner')
                    $('#userid + i').removeClass('fa-check-circle')
                    $('#userid + i').addClass('fa-times-circle')
                    icon.style.animation = ""
                    $('#submitbtn').prop('disabled',true)
                    $('#username_errormessage').html("Username doesn't exists please try again")
                }
                else{
                    $('#userid + i').removeClass('fa-spinner')
                    $('#userid + i').removeClass('fa-times-circle')
                    $('#userid + i').addClass('fa-check-circle')
                    icon.style.animation = ""
                    $('#username_errormessage').html("")
                    $('#submitbtn').prop('disabled',false)
                }
            },
            error:function(response){
                alert('Error Occured Please try again')
                icon.style.animation = ""
                $('#userid + i').css('transform','scale(0)')
            }
        })
    })
}

main()