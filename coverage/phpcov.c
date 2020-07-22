#include<stdio.h>
#include<stdio.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include<sys/types.h>
#include<string.h>
#include<errno.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<stdint.h>
#include<python2.7/Python.h>

#define SHM_SIZE 0x1000
#define SHM_KEY 0x1234

typedef struct covdata{
  char* snapshot;
  char* shmem;
} covdata;

covdata* cdata;
PyObject *init();
PyObject *evalCoverage();

PyObject *init(PyObject *self)
{
  int shmid = shmget(SHM_KEY, SHM_SIZE, 0644|IPC_CREAT);
  char* shmem = shmat(shmid, NULL, 0);
  memset(shmem,0,SHM_SIZE);
  cdata = (covdata*)malloc(sizeof(covdata));
  cdata->shmem = shmem;
  cdata->snapshot = (char*)malloc(SHM_SIZE);
  memset(cdata->snapshot,0,SHM_SIZE);
  Py_INCREF(Py_None);
  return Py_None;
}

PyObject *evalCoverage(PyObject *self)
{
  int newPathFound=0;
  for (int i=0; i<SHM_SIZE; i++)
  {
    uint8_t val = cdata->shmem[i];
    uint8_t oldVal = cdata->snapshot[i];
    for (int j=0; j<8; j++)
    {
      if ((val & (1<<j)) && !(oldVal & (1<<j)))
      {
        newPathFound++;
        oldVal |= (1<<j);
        cdata->snapshot[i]=oldVal;
      }
    }
  }

  return Py_BuildValue("i", newPathFound);
}

PyObject *getpoints(PyObject *self)
{
  char *points = (char*)calloc(1,((SHM_SIZE*3)+1));
  char temp[10]={0};
  for (int i=0; i<SHM_SIZE; i++)
  {
    sprintf(temp, "%02hhx", cdata->shmem[i]);
    strcat(points, temp);
  }
  return Py_BuildValue("s",points);
}

static PyMethodDef phpcovMethods[] = {
    {"evalCoverage",  evalCoverage, METH_VARARGS, "Execute a shell command."},
    {"init",  init, METH_VARARGS, "Execute a shell command."},
    {"getpoints",  getpoints, METH_VARARGS, "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initphpcov(void)
{
    (void) Py_InitModule("phpcov", phpcovMethods);
}
