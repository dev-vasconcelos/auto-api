using Microsoft.EntityFrameworkCore;
using $projectName.Models;

namespace ${projectName}.DataBase
{
    public class NpgContext : DbContext
    {
        public NpgContext(DbContextOptions<NpgContext> options) :
            base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
        }
    }
}
