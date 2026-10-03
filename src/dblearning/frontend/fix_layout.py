file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target_old = """      <div className="flex flex-col lg:flex-row gap-6 items-start">
        <div className="flex-1 min-w-0 w-full">
          {/* Filters */}
          <UserFilters 
            filters={filters} 
            setFilters={setFilters} 
            onFilter={handleFilter} 
            onReset={handleResetFilters} 
          />

          {/* Table */}
          <UserTable """

target_new = """      {/* Filters */}
      <div className="mb-6">
        <UserFilters 
          filters={filters} 
          setFilters={setFilters} 
          onFilter={handleFilter} 
          onReset={handleResetFilters} 
        />
      </div>

      <div className="flex flex-col lg:flex-row gap-6 items-start">
        <div className="flex-1 min-w-0 w-full">
          {/* Table */}
          <UserTable """

if target_old in content:
    content = content.replace(target_old, target_new)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Moved UserFilters outside the flex container successfully")
else:
    print("Target not found. Please check manually.")
