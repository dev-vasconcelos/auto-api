using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using ${projectName}.DataBase;
using ${projectName}.Models;
using ${projectName}.Repository.AbstractClass;
using ${projectName}.Repository.Interface;
using ${projectName}.Service.Interface;
using ${projectName}.Service.Models.Interface;

namespace ${projectName}.Service.AbstractClass
{
    public class AbstractServiceNpgsql<T> : IService<T> where T : AbstractEntity
    {
        protected IRepository<T> _repository;
        protected NpgContext _context;

        public AbstractServiceNpgsql(NpgContext context)
        {
            this._context = context;
            _repository = new RepositoryNpgsql<T>(context);
        }

        public AbstractServiceNpgsql()
        {

        }

        public virtual T Save(T entity)
        {
            _repository.Save(entity);

            return entity;
        }

        public virtual T Update(T entity)
        {
            _repository.Update(entity);

            return entity;
        }

        public virtual List<T> Get() => _repository.Get();
        public virtual T Get(T entity)
        {
            T t = _repository.Get(entity);
            allLoad(t);

            return _repository.Get(t);
        }

        public virtual T Get(long? id)
        {
            T t = _repository.Get(id);
            allLoad(t);

            return _repository.Get(t);
        }

        public virtual List<T> Get(Expression<Func<T, bool>> predicate, params string[] navProperties) => _repository.Get(predicate, navProperties);

        public virtual bool Delete(T entity)
        {
            return _repository.Delete(entity);
        }

        public virtual bool Delete(long? id)
        {
            return _repository.Delete(id);
        }

        private void allLoad(T generic)
        {
            foreach (var i in generic.GetType().GetProperties().ToList())
            {
                if (i.GetValue(generic) == null)
                {
                    /*funciona
                    dynamic v = Activator.CreateInstance(i.GetGetMethod().ReturnType);
                    if(v is AbstractEntity) {
                    */
                    if (i.GetGetMethod().ReturnType.GetInterfaces().Contains(typeof(IEntity)))
                    {
                        // _context.Entry(generic).Reference(g => g.VariavelReferencia).Load();
                        _context.Entry(generic).Reference(i.Name).Load();
                    }
                }
            }
        }
    }
}