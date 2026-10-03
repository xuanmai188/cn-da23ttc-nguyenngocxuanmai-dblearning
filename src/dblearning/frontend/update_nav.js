const fs = require('fs');
const path = 'D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx';
let content = fs.readFileSync(path, 'utf8');

// The replacement text
const searchStr = 'onClick={() => alert("Tính năng xem tất cả đang được phát triển")}';
const btn1 = 'onClick={() => navigate("/admin/users")}';
const btn2 = 'onClick={() => navigate("/admin/content")}';
const btn3 = 'onClick={() => navigate("/admin/reports")}';

// We replace the 1st, 2nd, and 3rd occurrence
let parts = content.split(searchStr);
if (parts.length === 4) {
    content = parts[0] + btn1 + parts[1] + btn2 + parts[2] + btn3 + parts[3];
    fs.writeFileSync(path, content, 'utf8');
    console.log('Successfully updated navigation for Xem tất cả buttons');
} else {
    console.log('Could not find exactly 3 occurrences. Found:', parts.length - 1);
}
