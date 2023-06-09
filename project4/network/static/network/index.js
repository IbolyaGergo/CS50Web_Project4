document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'edit') {

            // Hide edit button
            element.style.display = "none";

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

                // Show edit button
                element.style.display = 'block';

                // Remove textarea and save btn
                element.parentElement.removeChild(save_btn);
                element.parentElement.removeChild(textarea);
            });
        } else if (element.className === 'fa fa-heart') {
            // const post_id = parseInt(element.getAttribute('data-post_id'));
            const post_id = parseInt(element.dataset.post_id);
            console.log(post_id);
            fetch(`/like_post/${post_id}`, {
                method: 'PUT'
            });

            var num_of_likes = parseInt(element.parentElement.children[1].innerHTML);

            if (element.style.color === 'red') {
                element.style.color = 'grey';
                num_of_likes--;
            } else {
                element.style.color = 'red';
                num_of_likes++;
            }
            element.parentElement.children[1].innerHTML = num_of_likes;
            // console.log(element.parentElement.children[1].innerHTML);
        }
    });
});