using System.Collections.Generic;
using Rfid.DataBase;
using Rfid.DTO.AbstractClass;
using Rfid.Models;
using Rfid.Service.AbstractClass;

namespace Rfid.Commons.Helpers
{
    
    public class CollectionHandlerHelper<T, T2> where T : AbstractEntity
    // public class CollectionHandlerHelper<T, T2> where T : AbstractEntity where T2 : AbstractModelDTO<T, T2>
    {
        protected NpgContext _context;
        protected AbstractServiceNpgsql<T> _service;

        public CollectionHandlerHelper(NpgContext context)
        {
            this._context = context;
            this._service = new AbstractServiceNpgsql<T>(context);
        }

        public virtual ICollection<T> AddManyToMany(ICollection<T2> from, ICollection<T> target)
        {
            // foreach (T2 unitDTO in from)
            foreach (dynamic unitDTO in from)
            {
                T unit = unitDTO.ConvertFromDto(unitDTO);
                T tmp = _service.Get(unit);
                target.Add(tmp);
            }
            return target;
        }

        
    }
}
