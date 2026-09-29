import os
file_path = 'D:/DemoCN2026/dblearning/frontend/src/pages/Login.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for EyeIcon and EyeSlashIcon
if "EyeIcon" not in content:
    content = content.replace("import { motion } from 'framer-motion';", "import { motion } from 'framer-motion';\nimport { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';")

# Add state for showPassword
if "showPassword" not in content:
    content = content.replace("const [isLoading, setIsLoading] = useState(false);", "const [isLoading, setIsLoading] = useState(false);\n  const [showPassword, setShowPassword] = useState(false);")

# Update password input
password_field_original = '''<input
              type="password"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />'''

# If the exact match fails due to some spaces, we can use a simpler replace or regex
import re
new_password_field = '''<div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none pr-10"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeSlashIcon className="h-5 w-5" aria-hidden="true" />
                ) : (
                  <EyeIcon className="h-5 w-5" aria-hidden="true" />
                )}
              </button>
            </div>'''

content = re.sub(r'<input\s+type="password"[\s\S]*?onChange=\{\(e\) => setPassword\(e\.target\.value\)\}\s*/>', new_password_field, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Login.jsx updated with EyeIcon.")
