    let card_list_div = document.getElementById('item-list');
    const selected_tags = {
        type: new Set(),
        tags: new Set(),
        variant: new Set(),
        feature: new Set(),
        source: new Set()
    }
    const list_of_type = data['type'];
    const list_of_tags = data['tags'];
    const list_of_variant = data['variant'];
    const list_of_feature = data['feature'];
    const list_of_source = data['source'];

    generate_left_checkbox_list(list_of_type, 'list-type', 'type');
    generate_left_checkbox_list(list_of_tags, 'list-tags', 'tags');
    generate_left_checkbox_list(list_of_variant, 'list-variant', 'variant');
    generate_left_checkbox_list(list_of_feature, 'list-feature', 'feature');
    generate_left_checkbox_list(list_of_source, 'list-source', 'source');

    document.getElementById('show-types').checked = false;
    document.getElementById('show-tags').checked = false;
    document.getElementById('show-variant').checked = false;
    document.getElementById('show-feature').checked = false;
    document.getElementById('show-source').checked = false;


    function generate_left_checkbox_list(items, localisation, collection) {

        const container = document.getElementById(localisation);
        console.log(items)
        items.forEach(item => {
            const label = document.createElement("label");
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.value = item;

            checkbox.addEventListener("change", () => {
                if (collection === 'type') {
                    if (selected_tags.type.has(item)) {
                        selected_tags.type.delete(item)
                    } else selected_tags.type.add(item)
                }

                if (collection === 'tags') {
                    if (selected_tags.tags.has(item)) {
                        selected_tags.tags.delete(item)
                    } else selected_tags.tags.add(item)
                }
                if (collection === 'variant') {
                    if (selected_tags.variant.has(item)) {
                        selected_tags.variant.delete(item)
                    } else selected_tags.variant.add(item)
                }
                if (collection === 'feature') {
                    if (selected_tags.feature.has(item)) {
                        selected_tags.feature.delete(item)
                    } else selected_tags.feature.add(item)
                }
                if (collection === 'source') {
                    if (selected_tags.source.has(item)) {
                        selected_tags.source.delete(item)
                    } else selected_tags.source.add(item)
                }
            })

            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(" " + item));
            container.appendChild(label);
            container.appendChild(document.createElement("br"));
        });

    }

    document.getElementById('show-types').addEventListener("change", () => {
        document.getElementById('list-type').classList.toggle("show", document.getElementById('show-types').checked);
    });
    document.getElementById('show-tags').addEventListener("change", () => {
        document.getElementById('list-tags').classList.toggle("show", document.getElementById('show-tags').checked);
    });
    document.getElementById('show-source').addEventListener("change", () => {
        document.getElementById('list-source').classList.toggle("show", document.getElementById('show-source').checked);
    });
    document.getElementById('show-feature').addEventListener("change", () => {
        document.getElementById('list-feature').classList.toggle("show", document.getElementById('show-feature').checked);
    });
    document.getElementById('show-variant').addEventListener("change", () => {
        document.getElementById('list-variant').classList.toggle("show", document.getElementById('show-variant').checked);
    });

    function get_results() {
        card_list_div.innerHTML=''
        item_map.clear();
        fetch("search", {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                type: [...selected_tags.type],
                item_tags: [...selected_tags.tags],
                feature: [...selected_tags.feature],
                work_source: [...selected_tags.source],
                variant: [...selected_tags.variant]
            })
        }).then(response => {
            if (!response.ok) throw new Error("Błąd sieci!");
            return response.json();
        }).then(data => {
            console.log("Odpowiedź serwera:", data['received']);
            if (data['received']) {
                console.log('empty')
            }
            let json_data = JSON.parse(data['received'])
            json_data.forEach(item => {
            card_list_div.appendChild(generate_card(item))
            })
        }).catch(error => {
            console.error("Wystąpił błąd:", error);
        })
    }