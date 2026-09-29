file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_layout = """      {/* Summary Cards */}
      <UserStatsCards stats={stats} />

      <div className="flex flex-col lg:flex-row gap-6 items-start">
        <div className="flex-1 min-w-0 w-full">
          {/* Filters */}
          <UserFilters 
            filters={filters} 
            setFilters={setFilters} 
            onFilter={handleFilter} 
            onReset={handleResetFilters} 
          />

          {/* Table */}
          <UserTable 
            users={users} 
            loading={loading}
            page={page}
            limit={limit}
            total={total}
            setPage={setPage}
            setLimit={setLimit}
            onAction={handleAction}
          />
        </div>
        
        {/* Detail Panel */}
        {selectedUser && (
          <div className="w-full lg:w-[380px] shrink-0">
            <UserDetailPanel 
              user={selectedUser} 
              onClose={() => setSelectedUser(null)} 
            />
          </div>
        )}
      </div>"""

import re
# Replace from {/* Summary Cards */} to the end of the return statement
content = re.sub(r'\{\/\* Summary Cards \*\/\}.*?<\/div>\n  \);\n\}', new_layout + "\n    </div>\n  );\n}", content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserManagement.jsx layout")
