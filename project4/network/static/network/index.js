document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'edit') {
            // Create a textarea
            const textarea = document.createElement("TEXTAREA");
            textarea.className = "form-control";

            // Get the current post
            const post_body = element.parentElement.children[2];
            const curr_post = document.createTextNode(post_body.innerHTML);

            // Fill the textarea with the current post
            textarea.appendChild(curr_post);

            // Create save button
            const save_btn = document.createElement("button");
            save_btn.className = "btn btn-primary";
            save_btn.innerHTML = "Save";
            
            // Hide the current post
            post_body.style.display = 'none';

            // Add text area and save btn to the post
            element.parentElement.insertBefore(textarea, post_body);
            element.parentElement.insertBefore(save_btn, post_body);

            save_btn.addEventListener('click', () => {
                console.log(element.value);
                const post_id = parseInt(element.value);
                fetch(`/edit_post/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        post_body: textarea.value
                    })
                });
                // Change the post to the edited post
                post_body.innerHTML = textarea.value;

                // Show the edited post
                post_body.style.display = 'block';

                // Remove textarea and save btn
                element.parentElement.removeChild(save_btn);
                element.parentElement.removeChild(textarea);
            });
        }
    });
});