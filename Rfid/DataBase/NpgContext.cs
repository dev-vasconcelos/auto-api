using Microsoft.EntityFrameworkCore;
using Rfid.Models;

namespace Rfid.DataBase
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

