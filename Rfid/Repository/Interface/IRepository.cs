using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;

namespace Rfid.Repository.Interface {
    public interface IRepository<T> {
        T Save(T entity);
        Task<T> SaveAsync(T entity);
        IEnumerable<T> SaveRange(IEnumerable<T> entity);
        Task<IEnumerable<T>> SaveRangeAsync(IEnumerable<T> entity);

        T Update(T entity);
        bool Delete(T entity);

        bool Delete(long? id);

        List<T> Get();

        List<T> Get(Expression<Func<T, bool>> predicate, params string[] navProperties);
        T Get(T entity);

        T Get(long? id);
    }
}
