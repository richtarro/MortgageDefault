function saveDatabase(){
		if (save.checked){
      firstlastname.style.display="inline";
      FirstName.setAttribute('required',true);
      LastName.setAttribute('required',true);
		}
		else{ 
			FirstName.removeAttribute('required');
			LastName.removeAttribute('required');
			firstlastname.style.display="none";
		}
	}