const SelectDropdown= document.querySelector(".select-drop .title");
const dropIcon= document.querySelector('.select-drop .title > i');
const contentDisplay= document.querySelector('.select-drop .content');

var isOpen= false;
SelectDropdown.addEventListener("click", () => {
    if(!isOpen){
        dropIcon.style.transform= 'rotate(180deg)';
        contentDisplay.style.display= 'none';
    }else{
        dropIcon.style.transform= 'rotate(0deg)';
        contentDisplay.style.display= 'flex';
    }
    isOpen= !isOpen;
})