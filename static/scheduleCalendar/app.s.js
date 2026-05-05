document.addEventListener('DOMContentLoaded', () => {
    let selectedCareItems = [];

    // 調子のアイコンをクリックしたときの処理
    function setHealthStatus(status) {
        const healthStatusInput = document.getElementById('health-status-input');
        healthStatusInput.value = status;
        alert(`${status} を選択しました。`);

        // 選択状態のビジュアルを更新
        const icons = document.querySelectorAll('#health-status img');
        icons.forEach(icon => {
            icon.style.border = icon.title === status ? '2px solid #0b6502' : 'none';
        });
    }

    // ケア項目をクリックしたときの処理
    function toggleCareItem(item) {
        const index = selectedCareItems.indexOf(item);
        if (index === -1) {
            selectedCareItems.push(item);
            alert(`${item} を選択しました。`);
        } else {
            selectedCareItems.splice(index, 1);
            alert(`${item} を解除しました。`);
        }

        // 隠しフィールドに選択されたケア項目をセット
        document.getElementById('care-items-input').value = selectedCareItems.join(', ');

        // 選択状態のビジュアルを更新
        const icons = document.querySelectorAll('#care-items img');
        icons.forEach(icon => {
            icon.style.border = selectedCareItems.includes(icon.title) ? '2px solid #0b6502' : 'none';
        });
    }

    // アイコンにイベントリスナーを追加
    const healthIcons = document.querySelectorAll('#health-status img');
    healthIcons.forEach(icon => {
        icon.addEventListener('click', () => setHealthStatus(icon.title));
    });

    const careIcons = document.querySelectorAll('#care-items img');
    careIcons.forEach(icon => {
        icon.addEventListener('click', () => toggleCareItem(icon.title));
    });

    // フォーム送信時のバリデーション
    document.querySelector('form').addEventListener('submit', (event) => {
        const healthStatusInput = document.getElementById('health-status-input');
        const careItemsInput = document.getElementById('care-items-input');

        if (!healthStatusInput.value) {
            alert('調子を選択してください。');
            event.preventDefault(); // フォーム送信をキャンセル
            return;
        }

        if (!careItemsInput.value) {
            alert('ケア項目を選択してください。');
            event.preventDefault(); // フォーム送信をキャンセル
            return;
        }
    });
});

